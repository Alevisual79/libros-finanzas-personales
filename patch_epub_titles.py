"""
Patch EPUB titles: fix the BOM issue that caused book numbers to appear in titles.
Opens each EPUB as a zip, corrects the <dc:title> in content.opf and <title> in nav.xhtml,
then writes the corrected zip back.
"""
import os, re, zipfile, shutil, tempfile

BASE = r"c:\Users\usuario\Desktop\IA\Libros"

COLLECTIONS = [
    "AI_Artificial_Intelligence", "Applied_Psychology", "Entrepreneurship",
    "Health_Wellness", "Personal_Finance", "Productivity_Success",
    "Relationships_Communication", "IA_Inteligencia_Artificial",
    "Psicologia_Aplicada", "Emprendimiento", "Salud_Bienestar",
    "Finanzas_Personales", "Productividad_Exito", "Relaciones_Comunicacion",
]


def _md_title(md_path):
    """Read correct title from markdown (utf-8-sig strips BOM)."""
    with open(md_path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
    return ""


def _patch_epub(epub_path, correct_title):
    """Replace the wrong title in the EPUB zip without extracting everything."""
    tmp = epub_path + ".tmp"
    try:
        with zipfile.ZipFile(epub_path, "r") as zin, \
             zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as zout:

            for item in zin.infolist():
                data = zin.read(item.filename)

                if item.filename.endswith("content.opf"):
                    text = data.decode("utf-8")
                    # Replace <dc:title>ANYTHING</dc:title>
                    text = re.sub(
                        r'(<dc:title[^>]*>)[^<]*(</dc:title>)',
                        rf'\g<1>{_xml_escape(correct_title)}\g<2>',
                        text
                    )
                    data = text.encode("utf-8")

                elif item.filename.endswith("nav.xhtml") or \
                     item.filename.endswith("toc.ncx"):
                    text = data.decode("utf-8")
                    # Replace <title>ANYTHING</title>
                    text = re.sub(
                        r'(<title>)[^<]*(</title>)',
                        rf'\g<1>{_xml_escape(correct_title)}\g<2>',
                        text
                    )
                    # Also fix h1 in nav: <h1 id="toc-title">ANYTHING</h1>
                    text = re.sub(
                        r'(<h1[^>]*>)[^<]*(</h1>)',
                        rf'\g<1>{_xml_escape(correct_title)}\g<2>',
                        text,
                        count=1
                    )
                    data = text.encode("utf-8")

                zout.writestr(item, data)

        shutil.move(tmp, epub_path)
        return True
    except Exception as e:
        if os.path.exists(tmp):
            os.remove(tmp)
        return str(e)


def _xml_escape(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")


def main():
    total_ok = total_skip = total_err = 0

    for col in COLLECTIONS:
        col_path = os.path.join(BASE, col)
        if not os.path.isdir(col_path):
            continue

        ok = skip = err = 0
        for root, _, files in os.walk(col_path):
            for fname in sorted(files):
                if not fname.endswith(".epub"):
                    continue
                epub_path = os.path.join(root, fname)
                md_path   = os.path.splitext(epub_path)[0] + ".md"

                if not os.path.exists(md_path):
                    skip += 1
                    continue

                correct_title = _md_title(md_path)
                if not correct_title:
                    skip += 1
                    continue

                result = _patch_epub(epub_path, correct_title)
                if result is True:
                    ok += 1
                else:
                    err += 1
                    print(f"    ERROR {fname}: {result}")

        print(f"  {col}: {ok} corregidos | {skip} sin cambio | {err} errores")
        total_ok += ok; total_skip += skip; total_err += err

    print(f"\nTotal: {total_ok} corregidos | {total_skip} sin cambio | {total_err} errores")


if __name__ == "__main__":
    main()
