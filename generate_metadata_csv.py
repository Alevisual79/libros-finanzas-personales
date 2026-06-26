"""
KDP Metadata CSV Generator
Reads all 14 collection HTML files and outputs kdp_metadata.csv with
one row per book (1,414 total), ready to use as reference for KDP uploads.
"""

import os, re, csv, sys
sys.path.insert(0, r"C:\Users\usuario\AppData\Local\Temp\claude\c--Users-usuario-Desktop-IA-Libros\3bb01a1a-3911-43eb-a1d0-d356095fc6a0\scratchpad")
from generate_all_covers import (
    _extract_array, _extract_named_array, _parse_series_colors,
    _get_str, _get_int, _fallback_colors
)

BASE = r"c:\Users\usuario\Desktop\IA\Libros"
AUTHOR = "Enrique Padrón"

# ── Collection definitions ──────────────────────────────────────────────────

COLLECTIONS = [
    # (html_rel, images_rel, col_name, language, kdp_cat1, kdp_cat2, base_keywords)
    (
        "AI_Artificial_Intelligence/Covers/covers.html",
        "AI_Artificial_Intelligence/Covers/images",
        "AI & Artificial Intelligence", "en",
        "Computers & Technology > Artificial Intelligence",
        "Nonfiction > Science & Math > Technology",
        ["artificial intelligence", "machine learning", "AI", "technology", "future", "automation", "deep learning"],
    ),
    (
        "Applied_Psychology/Covers/covers.html",
        "Applied_Psychology/Covers/images",
        "Applied Psychology", "en",
        "Health, Fitness & Dieting > Psychology & Counseling > Applied Psychology",
        "Self-Help > Mental Health",
        ["psychology", "mental health", "behavior", "emotions", "self-help", "cognitive", "well-being"],
    ),
    (
        "Entrepreneurship/Covers/covers.html",
        "Entrepreneurship/Covers/images",
        "Entrepreneurship", "en",
        "Business & Money > Entrepreneurship & Small Business",
        "Self-Help > Success",
        ["entrepreneurship", "startup", "business", "success", "innovation", "leadership", "growth"],
    ),
    (
        "Health_Wellness/Covers/covers.html",
        "Health_Wellness/Covers/images",
        "Health and Wellness", "en",
        "Health, Fitness & Dieting > General",
        "Self-Help > Happiness",
        ["health", "wellness", "nutrition", "fitness", "sleep", "habits", "lifestyle"],
    ),
    (
        "Personal_Finance/Covers/covers.html",
        "Personal_Finance/Covers/images",
        "Personal Finance", "en",
        "Business & Money > Personal Finance",
        "Self-Help > Success",
        ["personal finance", "money", "investing", "savings", "financial freedom", "budgeting", "wealth"],
    ),
    (
        "Productivity_Success/Covers/covers.html",
        "Productivity_Success/Covers/images",
        "Productivity & Success", "en",
        "Self-Help > Productivity & Time Management",
        "Business & Money > Management & Leadership",
        ["productivity", "success", "time management", "habits", "focus", "goals", "performance"],
    ),
    (
        "Relationships_Communication/Covers/covers.html",
        "Relationships_Communication/Covers/images",
        "Relationships & Communication", "en",
        "Self-Help > Relationships",
        "Health, Fitness & Dieting > Psychology & Counseling",
        ["relationships", "communication", "love", "family", "social skills", "boundaries", "empathy"],
    ),
    (
        "IA_Inteligencia_Artificial/Portadas/portadas.html",
        "IA_Inteligencia_Artificial/Portadas/images",
        "IA e Inteligencia Artificial", "es",
        "Ordenadores e Internet > Inteligencia Artificial",
        "Ciencia y Naturaleza > Tecnología",
        ["inteligencia artificial", "machine learning", "IA", "tecnología", "automatización", "algoritmos", "futuro"],
    ),
    (
        "Psicologia_Aplicada/Portadas/portadas.html",
        "Psicologia_Aplicada/Portadas/images",
        "Psicologia Aplicada", "es",
        "Salud, Familia y Desarrollo Personal > Psicología",
        "Autoayuda",
        ["psicología", "salud mental", "emociones", "autoayuda", "comportamiento", "bienestar", "mente"],
    ),
    (
        "Emprendimiento/Portadas/portadas.html",
        "Emprendimiento/Portadas/images",
        "Emprendimiento", "es",
        "Economía, Empresa y Finanzas > Administración y Dirección de Empresas",
        "Autoayuda > Éxito personal",
        ["emprendimiento", "negocios", "startup", "éxito", "liderazgo", "empresa", "innovación"],
    ),
    (
        "Salud_Bienestar/Portadas/portadas.html",
        "Salud_Bienestar/Portadas/images",
        "Salud y Bienestar", "es",
        "Salud, Familia y Desarrollo Personal > Salud y Bienestar",
        "Autoayuda",
        ["salud", "bienestar", "nutrición", "hábitos", "sueño", "ejercicio", "estilo de vida"],
    ),
    (
        "Finanzas_Personales/Portadas/portadas.html",
        "Finanzas_Personales/Portadas/images",
        "Finanzas Personales", "es",
        "Economía, Empresa y Finanzas > Finanzas Personales",
        "Autoayuda > Éxito personal",
        ["finanzas personales", "dinero", "ahorro", "inversión", "libertad financiera", "deuda", "patrimonio"],
    ),
    (
        "Productividad_Exito/Portadas/portadas.html",
        "Productividad_Exito/Portadas/images",
        "Productividad y Exito", "es",
        "Autoayuda > Éxito personal",
        "Economía, Empresa y Finanzas > Administración",
        ["productividad", "éxito", "gestión del tiempo", "hábitos", "foco", "metas", "rendimiento"],
    ),
    (
        "Relaciones_Comunicacion/Portadas/portadas.html",
        "Relaciones_Comunicacion/Portadas/images",
        "Relaciones y Comunicacion", "es",
        "Autoayuda > Relaciones",
        "Salud, Familia y Desarrollo Personal > Psicología",
        ["relaciones", "comunicación", "amor", "familia", "límites", "empatía", "vínculos"],
    ),
]

# ── Helpers ─────────────────────────────────────────────────────────────────

def _get_bullets(block):
    """Extract bullets/sinopsis array as list of strings."""
    m = re.search(r'bullets\s*:\s*\[(.*?)\]', block, re.DOTALL)
    if not m:
        return []
    inner = m.group(1)
    items = re.findall(r"'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\"", inner)
    return [a or b for a, b in items if (a or b)]


def _build_description(rec, lang):
    """Build a KDP-ready description from available fields."""
    # Primary description
    desc = _get_str(rec, "sinopsis", "desc", "description", "descripcion")
    sub  = _get_str(rec, "sub", "subtitle", "subtitulo")
    tagline = _get_str(rec, "tagline")
    bullets = _get_bullets(rec)

    parts = []
    if desc:
        parts.append(desc.strip())
    elif sub:
        parts.append(sub.strip())

    if tagline and tagline not in parts:
        # Format as pull quote
        parts.append(tagline.strip())

    if bullets:
        bullet_char = "•"
        bullet_lines = "\n".join(f"{bullet_char} {b.strip()}" for b in bullets)
        if lang == "en":
            parts.append("What you'll discover:\n" + bullet_lines)
        else:
            parts.append("Lo que descubrirás:\n" + bullet_lines)

    return "\n\n".join(parts) if parts else sub


def _build_md_index(base):
    """Walk all collections and return {(col_folder, num): md_path}."""
    index = {}
    col_folders = [
        "AI_Artificial_Intelligence", "Applied_Psychology", "Entrepreneurship",
        "Health_Wellness", "Personal_Finance", "Productivity_Success",
        "Relationships_Communication", "IA_Inteligencia_Artificial",
        "Psicologia_Aplicada", "Emprendimiento", "Salud_Bienestar",
        "Finanzas_Personales", "Productividad_Exito", "Relaciones_Comunicacion",
    ]
    for col in col_folders:
        col_path = os.path.join(base, col)
        if not os.path.isdir(col_path):
            continue
        for root, _, files in os.walk(col_path):
            for fname in files:
                if not fname.endswith(".md"):
                    continue
                m = re.match(r'^(\d+)', fname)
                if m:
                    index[(col, int(m.group(1)))] = os.path.join(root, fname)
    return index


def _prologue_excerpt(md_path, max_chars=600):
    """Extract first 2 paragraphs after ## Prologue (or ## Prólogo)."""
    if not md_path or not os.path.exists(md_path):
        return ""
    in_prologue = False
    paragraphs = []
    current = []
    with open(md_path, encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if re.match(r'^##\s+(Prologue|Prólogo|Prologo)', stripped, re.IGNORECASE):
                in_prologue = True
                continue
            if in_prologue:
                if stripped.startswith("##"):
                    break  # next section
                if stripped == "---":
                    break
                if stripped:
                    current.append(stripped)
                elif current:
                    paragraphs.append(" ".join(current))
                    current = []
                    if len(paragraphs) >= 2:
                        break
    if current:
        paragraphs.append(" ".join(current))
    text = "\n\n".join(paragraphs)
    if len(text) > max_chars:
        text = text[:max_chars].rsplit(" ", 1)[0] + "…"
    return text


def _keywords_for_book(base_kws, title, sub, serie):
    """Pick 7 keywords: 4 from base collection list + 3 extracted from title/sub."""
    title_words = [w.lower() for w in re.findall(r'\b[a-záéíóúüñA-ZÁÉÍÓÚÜÑ]{5,}\b', title + " " + sub)
                   if w.lower() not in {"about", "through", "these", "their", "which", "where",
                                        "entre", "sobre", "hacia", "cuándo", "cómo", "para"}]
    extra = []
    seen = set(kw.lower() for kw in base_kws)
    for w in title_words:
        if w not in seen and len(extra) < 3:
            extra.append(w)
            seen.add(w)
    combined = (base_kws[:4] + extra)[:7]
    return ";".join(combined)


def _display_serie(serie_str, lang):
    """Strip internal codes, keep human-readable series names."""
    if not serie_str:
        return ""
    s = str(serie_str).strip()
    if re.match(r'^S\d{1,2}$', s):
        return ""
    if re.match(r'^Serie\s*\d+$', s, re.IGNORECASE):
        return ""
    # Remove "Book X of 10" or "Libro X de 10" suffix for series title
    s = re.sub(r'\s*[—\-–]\s*(Book|Libro)\s*\d+\s*(of|de)\s*\d+', '', s, flags=re.IGNORECASE)
    if s in ("Mother Book", "Libro Madre"):
        return s
    return s.strip()


def parse_books_meta(html_path):
    """Extended parse that also returns desc, bullets, serie index."""
    with open(html_path, encoding="utf-8") as f:
        html = f.read()

    series_colors = _parse_series_colors(html)
    # Also parse series names for index-based files (Finanzas style)
    series_names = {}
    series_raw = _extract_named_array(html, "SERIES") or _extract_named_array(html, "series")
    if series_raw:
        for rec in re.findall(r"\{[^{}]+\}", series_raw, re.DOTALL):
            sid = _get_int(rec, "id")
            nombre = _get_str(rec, "nombre", "name")
            if nombre:
                series_names[sid] = nombre

    raw = _extract_array(html)
    if not raw:
        raise ValueError(f"No books array in {html_path}")

    records = re.findall(r"\{[^{}]+\}", raw, re.DOTALL)
    books = []
    for rec in records:
        num   = _get_int(rec, "num", "numTotal", "id")
        title = (_get_str(rec, "title", "titulo") or _get_str(rec, "tituloLargo")).replace("\\n", " ").strip()
        sub   = _get_str(rec, "sub", "subtitle", "subtitulo")
        serie_raw = _get_str(rec, "serie")
        # For index-based series (Finanzas), look up name
        if not serie_raw:
            sid = _get_int(rec, "serie")
            serie_raw = series_names.get(sid, "")
        num_in_serie = _get_int(rec, "numSerie") or 0
        books.append({
            "num": num,
            "title": title,
            "sub": sub,
            "serie": serie_raw,
            "num_in_serie": num_in_serie,
            "rec_raw": rec,
        })
    return books


# ── Main ────────────────────────────────────────────────────────────────────

FIELDNAMES = [
    "collection", "language", "num", "title", "subtitle",
    "series_title", "volume_in_series",
    "author", "description", "keywords",
    "category_1", "category_2",
    "cover_path", "md_path",
]

out_path = os.path.join(BASE, "kdp_metadata.csv")
total = 0

# Build markdown file index once for all collections
print("Indexando archivos markdown...")
MD_INDEX = _build_md_index(BASE)
print(f"  {len(MD_INDEX)} archivos .md indexados")

# Map col_name → col_folder for index lookups
COL_NAME_TO_FOLDER = {
    "AI & Artificial Intelligence": "AI_Artificial_Intelligence",
    "Applied Psychology":           "Applied_Psychology",
    "Entrepreneurship":             "Entrepreneurship",
    "Health and Wellness":          "Health_Wellness",
    "Personal Finance":             "Personal_Finance",
    "Productivity & Success":       "Productivity_Success",
    "Relationships & Communication":"Relationships_Communication",
    "IA e Inteligencia Artificial": "IA_Inteligencia_Artificial",
    "Psicologia Aplicada":          "Psicologia_Aplicada",
    "Emprendimiento":               "Emprendimiento",
    "Salud y Bienestar":            "Salud_Bienestar",
    "Finanzas Personales":          "Finanzas_Personales",
    "Productividad y Exito":        "Productividad_Exito",
    "Relaciones y Comunicacion":    "Relaciones_Comunicacion",
}

with open(out_path, "w", encoding="utf-8-sig", newline="") as csvf:
    writer = csv.DictWriter(csvf, fieldnames=FIELDNAMES)
    writer.writeheader()

    for html_rel, images_rel, col_name, lang, cat1, cat2, base_kws in COLLECTIONS:
        html_path  = os.path.join(BASE, html_rel)
        images_dir = os.path.join(BASE, images_rel)
        col_folder = COL_NAME_TO_FOLDER.get(col_name, "")

        try:
            books = parse_books_meta(html_path)
        except Exception as e:
            print(f"ERROR {col_name}: {e}")
            continue

        col_written = 0
        for book in books:
            num   = book["num"]
            title = book["title"]
            sub   = book["sub"]
            serie = _display_serie(book["serie"], lang)
            num_in_serie = book["num_in_serie"]
            rec   = book["rec_raw"]

            # Find markdown path via index
            md_path = MD_INDEX.get((col_folder, num), "")

            # Description: ES uses HTML sinopsis+bullets; EN enriches with Prologue
            html_desc = _build_description(rec, lang)
            if lang == "en" and md_path:
                prologue = _prologue_excerpt(md_path, max_chars=700)
                if prologue:
                    tagline = _get_str(rec, "desc")
                    desc = f"{tagline}\n\n{prologue}" if tagline else prologue
                else:
                    desc = html_desc
            else:
                desc = html_desc

            keywords = _keywords_for_book(base_kws, title, sub, serie)
            cover_path = os.path.join(images_dir, f"{str(num).zfill(3)}.jpg")

            writer.writerow({
                "collection":       col_name,
                "language":         lang,
                "num":              num,
                "title":            title,
                "subtitle":         sub,
                "series_title":     serie,
                "volume_in_series": num_in_serie if num_in_serie else num,
                "author":           AUTHOR,
                "description":      desc,
                "keywords":         keywords,
                "category_1":       cat1,
                "category_2":       cat2,
                "cover_path":       cover_path,
                "md_path":          md_path,
            })
            col_written += 1

        total += col_written
        print(f"  {col_name}: {col_written} libros")

print(f"\nTotal: {total} filas -> {out_path}")
