"""
KDP Upload Automation — Playwright (headed mode)
================================================
Uso:
  python kdp_upload.py                     # sube todos los libros pendientes
  python kdp_upload.py --collection "Applied Psychology"  # solo una coleccion
  python kdp_upload.py --limit 10          # maximo N libros esta sesion
  python kdp_upload.py --start 50          # empieza desde el libro N del CSV

El script abre Chrome, espera que el usuario haga login en KDP,
luego automatiza los 3 pasos de cada libro. Progreso en kdp_progress.json.
"""

import os, csv, json, time, random, sys, argparse, traceback
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

BASE          = r"c:\Users\usuario\Desktop\IA\Libros"
CSV_PATH      = os.path.join(BASE, "kdp_metadata.csv")
PROGRESS_PATH = os.path.join(BASE, "kdp_progress.json")
ERRORS_DIR    = os.path.join(BASE, "kdp_errors")
KDP_BOOKSHELF = "https://kdp.amazon.com/en_US/bookshelf"
KDP_NEW_URL   = "https://kdp.amazon.com/en_US/title-setup/kindle/new/details"

DELAY_ACTION  = 0.8   # segundos entre acciones dentro de un campo
DELAY_BOOK    = 20    # segundos entre libros (para parecer humano)
TIMEOUT       = 30000 # ms de espera para elementos
DESC_MAX      = 4000  # límite de caracteres en descripción KDP


# ── Progress tracking ───────────────────────────────────────────────────────

def load_progress():
    if os.path.exists(PROGRESS_PATH):
        with open(PROGRESS_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {"completed": [], "failed": [], "last_run": None}

def save_progress(prog):
    prog["last_run"] = datetime.now().isoformat()
    with open(PROGRESS_PATH, "w", encoding="utf-8") as f:
        json.dump(prog, f, indent=2, ensure_ascii=False)

def book_id(row):
    return f"{row['collection']}::{row['num']}"


# ── CSV loading ─────────────────────────────────────────────────────────────

def load_books(collection_filter=None, start=0, limit=None):
    with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if collection_filter:
        rows = [r for r in rows if r["collection"] == collection_filter]
    rows = rows[start:]
    if limit:
        rows = rows[:limit]
    return rows


# ── Human-like helpers ──────────────────────────────────────────────────────

def wait(s=None):
    time.sleep(s or DELAY_ACTION + random.uniform(0.1, 0.4))

def slow_type(locator, text, clear=True):
    """Type text at human speed."""
    if clear:
        locator.triple_click()
        wait(0.3)
    locator.type(text, delay=40 + random.randint(0, 30))
    wait(0.4)

def safe_click(locator, timeout=TIMEOUT):
    locator.wait_for(state="visible", timeout=timeout)
    locator.scroll_into_view_if_needed()
    wait(0.3)
    locator.click()
    wait(0.5)


# ── Page 1: Details ─────────────────────────────────────────────────────────

def fill_details(page, book):
    print(f"    [1/3] Detalles...")

    # Title
    title_field = page.locator("input[id*='title']:not([id*='subtitle']):not([id*='series'])")
    slow_type(title_field.first, book["title"])

    # Subtitle
    if book.get("subtitle"):
        sub = page.locator("input[id*='subtitle']")
        if sub.count() > 0:
            slow_type(sub.first, book["subtitle"])

    # Series
    if book.get("series_title"):
        # Click "Add series" if not expanded
        add_series = page.locator("text=Add series, volume number or edition")
        if add_series.count() > 0:
            safe_click(add_series.first)
            wait()
        series_input = page.locator("input[id*='series-title'], input[placeholder*='series' i]")
        if series_input.count() > 0:
            slow_type(series_input.first, book["series_title"])
        vol_input = page.locator("input[id*='volume'], input[placeholder*='volume' i]")
        if vol_input.count() > 0:
            slow_type(vol_input.first, str(book.get("volume_in_series", "")))

    # Author — KDP splits into first/last name
    author = book.get("author", "Enrique Padrón")
    parts = author.strip().split(" ", 1)
    first_name = parts[0]
    last_name  = parts[1] if len(parts) > 1 else ""
    fn = page.locator("input[id*='first-name'], input[placeholder*='First' i]")
    ln = page.locator("input[id*='last-name'],  input[placeholder*='Last' i]")
    if fn.count() > 0: slow_type(fn.first, first_name)
    if ln.count() > 0: slow_type(ln.first, last_name)

    # Description — KDP uses a textarea or CKEditor (max 4000 chars)
    desc = book.get("description", "")[:DESC_MAX]
    if desc:
        # Try plain textarea first
        desc_ta = page.locator("textarea[id*='description'], textarea[name*='description']")
        if desc_ta.count() > 0:
            slow_type(desc_ta.first, desc)
        else:
            # CKEditor: inject via JS
            try:
                page.evaluate(f"""
                    var editors = Object.keys(CKEDITOR && CKEDITOR.instances || {{}});
                    if (editors.length) CKEDITOR.instances[editors[0]].setData({json.dumps(desc)});
                """)
                wait()
            except Exception:
                # Fallback: click into iframe and type
                frame = page.frame_locator("iframe.cke_wysiwyg_frame")
                if frame:
                    body = frame.locator("body")
                    body.click()
                    page.keyboard.press("Control+a")
                    page.keyboard.type(desc[:4000])
                    wait()

    # Keywords (7 fields)
    kws = book.get("keywords", "").split(";")[:7]
    kw_inputs = page.locator("input[id*='keyword']")
    for i, kw in enumerate(kws):
        if i < kw_inputs.count():
            slow_type(kw_inputs.nth(i), kw.strip())

    # Language
    lang_code = book.get("language", "en")
    lang_label = "English" if lang_code == "en" else "Spanish"
    lang_sel = page.locator("select[id*='language']")
    if lang_sel.count() > 0:
        lang_sel.first.select_option(label=lang_label)
        wait()

    # Click Save & Continue (or Next)
    _click_next(page)


# ── Page 2: Content ─────────────────────────────────────────────────────────

def _wait_upload_success(page, timeout=120000):
    """Wait for KDP upload success — handles different success message variants."""
    page.locator(
        "text=Upload successful, text=uploaded successfully, "
        "text=Your manuscript has been received, text=Cover uploaded"
    ).first.wait_for(state="visible", timeout=timeout)
    wait(2)


def fill_content(page, book):
    print(f"    [2/3] Subiendo EPUB y portada...")

    # DRM — enable (default is on, just make sure)
    drm = page.locator("input[type='radio'][value*='drm'], input[id*='drm-yes']")
    if drm.count() > 0:
        drm.first.check()
        wait()

    # Upload manuscript (EPUB)
    epub_path = book.get("md_path", "")
    if epub_path:
        epub_path = os.path.splitext(epub_path)[0] + ".epub"
    if epub_path and os.path.exists(epub_path):
        ms_input = page.locator("input[type='file'][accept*='epub'], input[type='file'][id*='manuscript']")
        if ms_input.count() > 0:
            ms_input.first.set_input_files(epub_path)
            print(f"      EPUB: {os.path.basename(epub_path)}")
            _wait_upload_success(page, timeout=180000)
    else:
        print(f"      AVISO: EPUB no encontrado para libro {book['num']}")

    # Upload cover image (JPG)
    cover_path = book.get("cover_path", "")
    if cover_path and os.path.exists(cover_path):
        cover_input = page.locator(
            "input[type='file'][accept*='jpg'], input[type='file'][accept*='jpeg'], "
            "input[type='file'][id*='cover']"
        )
        if cover_input.count() > 0:
            cover_input.first.set_input_files(cover_path)
            print(f"      Cover: {os.path.basename(cover_path)}")
            _wait_upload_success(page, timeout=60000)
    else:
        print(f"      AVISO: portada no encontrada para libro {book['num']}")

    _click_next(page)


# ── Page 2b: Categories (called from fill_details after language) ────────────

def fill_categories(page, book):
    """Try to set KDP categories from category_1 / category_2 in CSV.
    KDP uses a modal tree selector — we navigate by clicking breadcrumbs."""
    cat1 = book.get("category_1", "")
    cat2 = book.get("category_2", "")
    if not cat1:
        return

    set_cat_btn = page.locator(
        "button:has-text('Set Categories'), button:has-text('Browse Categories'), "
        "a:has-text('Set Categories')"
    )
    if set_cat_btn.count() == 0:
        print(f"      INFO: botón de categorías no encontrado, saltando.")
        return

    for cat_str in [cat1, cat2]:
        if not cat_str:
            continue
        # Open modal
        if set_cat_btn.count() > 0:
            safe_click(set_cat_btn.first)
            wait(1.5)

        # Navigate tree: split by ' > '
        crumbs = [c.strip() for c in cat_str.split(">")]
        for crumb in crumbs:
            crumb_loc = page.locator(f"text={crumb}").first
            try:
                crumb_loc.wait_for(state="visible", timeout=5000)
                safe_click(crumb_loc)
            except Exception:
                print(f"      AVISO: categoría '{crumb}' no encontrada en modal.")
                break

        # Confirm selection
        add_btn = page.locator("button:has-text('Add'), button:has-text('Select'), button:has-text('Done')")
        if add_btn.count() > 0:
            safe_click(add_btn.first)
            wait(1)

    print(f"      Categorías: {cat1[:40]}")


# ── Page 3: Pricing ─────────────────────────────────────────────────────────

def fill_pricing(page, book, publish=False):
    print(f"    [3/3] Precio...")

    # KDP Select — NO (optar por distribución amplia)
    no_select = page.locator(
        "input[id*='select-no'], input[value*='not-enroll'], "
        "label:has-text('Not enrolled')"
    )
    if no_select.count() > 0:
        no_select.first.click()
        wait()

    # Territories — worldwide
    worldwide = page.locator(
        "input[value='world'], input[id*='worldwide'], "
        "label:has-text('All territories')"
    )
    if worldwide.count() > 0:
        worldwide.first.click()
        wait()

    # Royalty plan — 70% si precio >= $2.99, 35% si precio < $2.99
    price = float(book.get("price_usd", 2.99))
    if price >= 2.99:
        r70 = page.locator("input[value='70'], input[id*='royalty-70'], label:has-text('70%')")
        if r70.count() > 0:
            r70.first.click()
            wait()
    else:
        r35 = page.locator("input[value='35'], input[id*='royalty-35'], label:has-text('35%')")
        if r35.count() > 0:
            r35.first.click()
            wait()

    # Price USD
    price_input = page.locator(
        "input[id*='list-price-us'], input[id*='price-us'], input[placeholder*='USD' i]"
    )
    if price_input.count() > 0:
        slow_type(price_input.first, f"{price:.2f}")

    # Price EUR (usar precio USD si no hay específico)
    price_eur = float(book.get("price_eur", price))
    eur_input = page.locator(
        "input[id*='list-price-eu'], input[id*='price-eur'], input[placeholder*='EUR' i]"
    )
    if eur_input.count() > 0:
        slow_type(eur_input.first, f"{price_eur:.2f}")

    wait(1)

    # Publish o Save as Draft
    if publish:
        pub_btn = page.locator("button:has-text('Publish'), button:has-text('Submit for Review')")
        if pub_btn.count() > 0:
            safe_click(pub_btn.first)
            print(f"      Enviado para publicación.")
            return
        print(f"      AVISO: botón Publish no encontrado, guardando como borrador.")

    draft_btn = page.locator("button:has-text('Save as Draft'), input[value*='Draft']")
    if draft_btn.count() > 0:
        safe_click(draft_btn.first)
        print(f"      Guardado como borrador.")
    else:
        print(f"      AVISO: no se encontro boton de guardar. Toma control manual.")
        input("Presiona ENTER cuando hayas guardado manualmente...")


# ── Next button helper ──────────────────────────────────────────────────────

def _click_next(page):
    """Click Save & Continue / Next on any KDP page."""
    wait()
    btn = page.locator(
        "button:has-text('Save and Continue'), "
        "button:has-text('Save & Continue'), "
        "button:has-text('Next'), "
        "input[value*='Save and Continue'], "
        "input[value*='Next']"
    )
    if btn.count() == 0:
        raise RuntimeError("No se encontro boton de siguiente pagina")
    safe_click(btn.first)
    wait(2)


# ── Main upload flow ────────────────────────────────────────────────────────

def upload_one(page, book, publish=False):
    """Upload one book through all 3 KDP pages."""
    page.goto(KDP_NEW_URL)
    page.wait_for_load_state("networkidle", timeout=TIMEOUT)
    wait(2)

    fill_details(page, book)
    fill_categories(page, book)
    page.wait_for_load_state("networkidle", timeout=TIMEOUT)
    wait(1)

    fill_content(page, book)
    page.wait_for_load_state("networkidle", timeout=TIMEOUT)
    wait(1)

    fill_pricing(page, book, publish=publish)
    wait(3)


# ── Entry point ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="KDP Upload Automation")
    parser.add_argument("--collection", default=None, help="Solo esta coleccion")
    parser.add_argument("--limit",      type=int, default=None, help="Max libros esta sesion")
    parser.add_argument("--start",      type=int, default=0,    help="Empezar desde fila N del CSV")
    parser.add_argument("--publish",    action="store_true",    help="Publicar en vez de borrador")
    args = parser.parse_args()

    os.makedirs(ERRORS_DIR, exist_ok=True)
    books    = load_books(args.collection, args.start, args.limit)
    progress = load_progress()
    pending  = [b for b in books if book_id(b) not in progress["completed"]]

    print(f"\nKDP Upload Automation")
    print(f"Libros pendientes: {len(pending)}")
    print(f"Progreso guardado en: {PROGRESS_PATH}")
    print(f"\nAbriendo Chrome...\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=300,
            args=["--start-maximized"]
        )
        ctx  = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # Step 1: Manual login
        page.goto(KDP_BOOKSHELF)
        print("=" * 60)
        print("PASO 1: Inicia sesion en KDP en la ventana del navegador.")
        print("Cuando estes en el Bookshelf (lista de libros), presiona ENTER aqui.")
        print("=" * 60)
        input()

        # Step 2: Process books
        ok = fail = 0
        for i, book in enumerate(pending, 1):
            bid = book_id(book)
            num = book.get("num", "?")
            title = book.get("title", "?")[:50]
            print(f"\n[{i}/{len(pending)}] Libro {num}: {title}")

            try:
                upload_one(page, book, publish=args.publish)
                progress["completed"].append(bid)
                save_progress(progress)
                ok += 1
                print(f"    OK ({ok} completados, {fail} errores)")

                # Human-like pause between books
                pause = DELAY_BOOK + random.uniform(-5, 10)
                print(f"    Pausa {pause:.0f}s...")
                time.sleep(pause)

            except Exception as e:
                fail += 1
                err_info = {"id": bid, "title": title, "error": str(e), "time": datetime.now().isoformat()}
                progress["failed"].append(err_info)
                save_progress(progress)

                # Screenshot for debugging
                shot = os.path.join(ERRORS_DIR, f"error_{bid.replace('::', '_').replace(' ', '_')}.png")
                try:
                    page.screenshot(path=shot)
                except Exception:
                    pass

                print(f"    ERROR: {e}")
                print(f"    Screenshot: {shot}")
                print(f"    Presiona ENTER para continuar con el siguiente libro...")
                input()

        browser.close()

    print(f"\nSesion terminada: {ok} OK | {fail} errores")
    print(f"Progreso: {PROGRESS_PATH}")

if __name__ == "__main__":
    main()
