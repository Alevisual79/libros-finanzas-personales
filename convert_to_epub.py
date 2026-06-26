"""
EPUB Batch Converter — KDP ready
Converts all 1,414 markdown manuscripts to EPUB3 using pandoc.
- Embeds the matching cover image
- Passes title, author, language, series metadata
- Skips already-converted files (resume-friendly)
- Outputs each .epub next to its .md file
"""

import os, re, subprocess

BASE   = r"c:\Users\usuario\Desktop\IA\Libros"
PANDOC = (
    r"C:\Users\usuario\AppData\Local\Microsoft\WinGet\Packages"
    r"\JohnMacFarlane.Pandoc_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\pandoc-3.10\pandoc.exe"
)
AUTHOR = "Enrique Padrón"

# Map: collection_folder → (cover_images_subdir, language)
COLLECTIONS = {
    "AI_Artificial_Intelligence":  ("Covers/images",   "en"),
    "Applied_Psychology":           ("Covers/images",   "en"),
    "Entrepreneurship":             ("Covers/images",   "en"),
    "Health_Wellness":              ("Covers/images",   "en"),
    "Personal_Finance":             ("Covers/images",   "en"),
    "Productivity_Success":         ("Covers/images",   "en"),
    "Relationships_Communication":  ("Covers/images",   "en"),
    "IA_Inteligencia_Artificial":   ("Portadas/images", "es"),
    "Psicologia_Aplicada":          ("Portadas/images", "es"),
    "Emprendimiento":               ("Portadas/images", "es"),
    "Salud_Bienestar":              ("Portadas/images", "es"),
    "Finanzas_Personales":          ("Portadas/images", "es"),
    "Productividad_Exito":          ("Portadas/images", "es"),
    "Relaciones_Comunicacion":      ("Portadas/images", "es"),
}

# Simple KDP-friendly CSS embedded in every EPUB
EPUB_CSS = """
body { font-family: Georgia, serif; font-size: 1em; line-height: 1.6;
       margin: 1em 1.5em; color: #1a1a1a; }
h1 { font-size: 1.8em; font-weight: bold; text-align: center;
     margin: 2em 0 0.3em; page-break-before: always; }
h2 { font-size: 1.3em; font-weight: bold; margin: 1.5em 0 0.5em; }
h3 { font-size: 1.1em; font-weight: bold; margin: 1.2em 0 0.4em; }
p  { margin: 0 0 0.8em; text-indent: 1.2em; }
p:first-of-type, h1 + p, h2 + p, h3 + p { text-indent: 0; }
blockquote { border-left: 3px solid #ccc; margin: 1em 2em;
             padding-left: 1em; font-style: italic; color: #555; }
hr { border: none; border-top: 1px solid #ccc; margin: 2em auto; width: 60%; }
strong { font-weight: bold; }
em { font-style: italic; }
"""

CSS_PATH = os.path.join(BASE, "_epub_style.css")


def _write_css():
    # If external file exists, use it (allows editing without touching this script)
    if os.path.exists(CSS_PATH):
        return
    with open(CSS_PATH, "w", encoding="utf-8") as f:
        f.write(EPUB_CSS)


def _book_num(md_path):
    """Extract leading number from filename: '11_Title.md' → 11"""
    m = re.match(r'^(\d+)', os.path.basename(md_path))
    return int(m.group(1)) if m else None


def _parse_md_header(md_path):
    """Return (title, subtitle, series_line) from first 6 lines of markdown."""
    title = subtitle = series_line = ""
    with open(md_path, encoding="utf-8-sig") as f:  # utf-8-sig strips BOM
        for i, line in enumerate(f):
            line = line.strip()
            if not title and line.startswith("# "):
                title = line[2:].strip()
            elif not subtitle and line.startswith("## "):
                subtitle = line[3:].strip()
            elif not series_line and line.startswith("**Series") or \
                 (line.startswith("**Serie") and not series_line):
                series_line = line.strip("*").strip()
            if i > 10:
                break
    return title, subtitle, series_line


def convert(md_path, cover_path, lang):
    out_path = os.path.splitext(md_path)[0] + ".epub"
    if os.path.exists(out_path):
        return "skip"

    title, subtitle, series_line = _parse_md_header(md_path)
    if not title:
        title = os.path.splitext(os.path.basename(md_path))[0].replace("_", " ")

    cmd = [
        PANDOC, md_path,
        "-o", out_path,
        "-t", "epub3",
        "--standalone",
        f"--css={CSS_PATH}",
        "--metadata", f"title={title}",
        "--metadata", f"author={AUTHOR}",
        "--metadata", f"lang={lang}",
    ]
    if subtitle:
        cmd += ["--metadata", f"subtitle={subtitle}"]
    if series_line:
        cmd += ["--metadata", f"series={series_line}"]
    if cover_path and os.path.exists(cover_path):
        cmd += [f"--epub-cover-image={cover_path}"]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return f"ERROR: {result.stderr[:120]}"
    return "ok"


def main():
    _write_css()
    total_ok = total_skip = total_err = 0

    for col_folder, (cover_subdir, lang) in COLLECTIONS.items():
        col_path    = os.path.join(BASE, col_folder)
        cover_dir   = os.path.join(col_path, cover_subdir)
        if not os.path.isdir(col_path):
            print(f"  MISSING: {col_folder}")
            continue

        md_files = []
        for root, _, files in os.walk(col_path):
            for fname in sorted(files):
                if fname.endswith(".md"):
                    md_files.append(os.path.join(root, fname))

        ok = skip = err = 0
        for md_path in md_files:
            num = _book_num(md_path)
            cover_path = ""
            if num is not None:
                cover_path = os.path.join(cover_dir, f"{str(num).zfill(3)}.jpg")

            status = convert(md_path, cover_path, lang)
            if status == "ok":
                ok += 1
            elif status == "skip":
                skip += 1
            else:
                err += 1
                print(f"    {os.path.basename(md_path)}: {status}")

            done = ok + skip + err
            if done % 100 == 0:
                print(f"  [{col_folder}] {done}/{len(md_files)} procesados...")

        print(f"  {col_folder}: {ok} nuevos | {skip} ya existian | {err} errores")
        total_ok += ok; total_skip += skip; total_err += err

    print(f"\nTotal: {total_ok} convertidos | {total_skip} ya existian | {total_err} errores")


if __name__ == "__main__":
    main()
