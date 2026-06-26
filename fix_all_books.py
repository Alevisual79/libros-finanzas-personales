"""
fix_all_books.py — Correcciones masivas en todos los libros (1428 archivos .md)

Cambios aplicados:
  1. Disclaimer/Aviso legal → solo la frase final
  2. Enumeraciones inline (1) X (2) Y → una por línea
  3. Enumeraciones a) X b) Y → una por línea
  4. Ortografía básica: dobles espacios, "cómo" comparativo en ES
"""

import os, re, sys

BASE = r"c:\Users\usuario\Desktop\IA\Libros"

COLLECTIONS_EN = [
    "AI_Artificial_Intelligence", "Applied_Psychology", "Entrepreneurship",
    "Health_Wellness", "Personal_Finance", "Productivity_Success",
    "Relationships_Communication",
]
COLLECTIONS_ES = [
    "IA_Inteligencia_Artificial", "Psicologia_Aplicada", "Emprendimiento",
    "Salud_Bienestar", "Finanzas_Personales", "Productividad_Exito",
    "Relaciones_Comunicacion",
]

# ── 1. Disclaimer ────────────────────────────────────────────────────────────

DISC_EN_SHORT = "> **Disclaimer:** The use of the information in this book is the sole responsibility of the reader."
DISC_ES_SHORT = "> **Aviso legal:** El uso de la información de este libro es responsabilidad exclusiva del lector."

# Match the entire blockquote line (may span multiple lines if soft-wrapped,
# but in practice these are single long lines)
RE_DISC_EN = re.compile(
    r'>\s+\*\*Disclaimer:\*\*[^\n]*(?:\n>[^\n]*)*',
    re.MULTILINE
)
RE_DISC_ES = re.compile(
    r'>\s+\*\*Aviso legal:\*\*[^\n]*(?:\n>[^\n]*)*',
    re.MULTILINE
)

def fix_disclaimer(text, lang):
    if lang == "en":
        return RE_DISC_EN.sub(DISC_EN_SHORT, text)
    return RE_DISC_ES.sub(DISC_ES_SHORT, text)


# ── 2 & 3. Inline enumerations ───────────────────────────────────────────────

def _split_inline(line, pattern):
    """
    Given a line containing inline list markers (e.g. '(1)' or 'a)'),
    split at each marker and return preamble + list items.
    Returns None if fewer than 2 items found.
    """
    parts = re.split(pattern, line)
    # parts alternates: text, marker, text, marker, text ...
    # With capturing group: [preamble, mark1, content1, mark2, content2, ...]
    if len(parts) < 5:      # need at least preamble + 2 items
        return None
    preamble = parts[0].rstrip()
    items = []
    for i in range(1, len(parts) - 1, 2):
        marker  = parts[i]
        content = parts[i + 1].strip() if (i + 1) < len(parts) else ""
        if content:
            items.append((marker, content))
    if len(items) < 2:
        return None
    return preamble, items


def fix_inline_enumerations(text):
    lines = text.split('\n')
    out   = []
    for line in lines:
        # Skip headings, blockquotes, tables, already-formatted list items
        stripped = line.lstrip()
        if stripped.startswith(('#', '> ', '| ')):
            out.append(line)
            continue
        if re.match(r'^[-*]\s', stripped):   # bullet: "- item" or "* item"
            out.append(line)
            continue
        if re.match(r'^\d+\.\s', stripped):  # numbered: "1. item"
            out.append(line)
            continue

        # Pattern: (1) ... (2) ... (3) ...
        if re.search(r'\(\d+\).*\(\d+\)', line):
            result = _split_inline(line, r'\s*\((\d+)\)\s*')
            if result:
                preamble, items = result
                new_line = preamble + '\n\n' + '\n'.join(
                    f"{m}. {c}" for m, c in items
                )
                out.append(new_line)
                continue

        # Pattern: a) ... b) ... c) ...
        if re.search(r'\b[a-e]\).*\b[b-f]\)', line):
            result = _split_inline(line, r'\s*\b([a-f])\)\s*')
            if result:
                preamble, items = result
                new_line = preamble + '\n\n' + '\n'.join(
                    f"{m}) {c}" for m, c in items
                )
                out.append(new_line)
                continue

        out.append(line)
    return '\n'.join(out)


# ── 4. Spelling cleanup ──────────────────────────────────────────────────────

# Double spaces
RE_DOUBLE_SPACE = re.compile(r'(?<!\n)  +')

# ES: "cómo" used as comparison (se siente cómo, funciona cómo, etc.)
# "cómo" is interrogative/exclamative; "como" is comparative
# Safe pattern: verb + "cómo" + article/adjective/noun (not a question)
RE_COMO_ERROR = re.compile(
    r'\b(se siente|funciona|parece|actúa|actua|opera|trabaja|se comporta|'
    r'es visto|se presenta|se manifiesta|se describe|se muestra|suena|'
    r'resulta|aparece)\s+cómo\b'
)

def fix_spelling(text, lang):
    # Double spaces (not in code blocks or URLs)
    text = RE_DOUBLE_SPACE.sub(' ', text)
    # ES specific
    if lang == "es":
        text = RE_COMO_ERROR.sub(lambda m: m.group(0).replace('cómo', 'como'), text)
    return text


# ── Main loop ────────────────────────────────────────────────────────────────

def collect_md_files():
    files = []
    for col in COLLECTIONS_EN:
        col_path = os.path.join(BASE, col)
        if not os.path.isdir(col_path):
            continue
        for root, _, fnames in os.walk(col_path):
            for f in fnames:
                if f.endswith('.md'):
                    files.append((os.path.join(root, f), "en"))
    for col in COLLECTIONS_ES:
        col_path = os.path.join(BASE, col)
        if not os.path.isdir(col_path):
            continue
        for root, _, fnames in os.walk(col_path):
            for f in fnames:
                if f.endswith('.md'):
                    files.append((os.path.join(root, f), "es"))
    return files


def process_file(path, lang):
    with open(path, encoding="utf-8-sig") as f:
        original = f.read()

    text = original
    text = fix_disclaimer(text, lang)
    text = fix_inline_enumerations(text)
    text = fix_spelling(text, lang)

    if text == original:
        return False   # no change

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return True


def main():
    dry_run = "--dry-run" in sys.argv

    files = collect_md_files()
    print(f"Archivos .md encontrados: {len(files)}")
    if dry_run:
        print("(DRY RUN — no se guardan cambios)\n")

    changed = disc_fixed = enum_fixed = spell_fixed = 0

    for path, lang in files:
        with open(path, encoding="utf-8-sig") as f:
            original = f.read()

        text = original

        # Track what changed
        after_disc = fix_disclaimer(text, lang)
        if after_disc != text:
            disc_fixed += 1
        text = after_disc

        after_enum = fix_inline_enumerations(text)
        if after_enum != text:
            enum_fixed += 1
        text = after_enum

        after_spell = fix_spelling(text, lang)
        if after_spell != text:
            spell_fixed += 1
        text = after_spell

        if text != original:
            changed += 1
            if not dry_run:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text)

    print(f"\nResultados:")
    print(f"  Archivos modificados:       {changed}/{len(files)}")
    print(f"  Disclaimers acortados:      {disc_fixed}")
    print(f"  Enumeraciones reformateadas:{enum_fixed}")
    print(f"  Correcciones ortografía:    {spell_fixed}")
    if dry_run:
        print("\n[DRY RUN completado — ejecuta sin --dry-run para aplicar cambios]")
    else:
        print("\nListo. Recuerda regenerar los EPUBs con:")
        print("  python regenerate_epubs.py")


if __name__ == "__main__":
    main()
