"""
Añade una línea en blanco entre líneas consecutivas del tipo:
  **X — Palabra:** definición.
  **Y — Palabra:** definición.

Sin línea en blanco entre ellas, pandoc las une en un único párrafo.
Con línea en blanco, cada una aparece como párrafo separado (línea propia) en el EPUB.
"""
import os, re

BASE = r'c:\Users\usuario\Desktop\IA\Libros'

# Coincide con "**X — Palabra..." (letra mayúscula + guion largo)
RE_ACRO = re.compile(r'^\*\*[A-ZÁÉÍÓÚÜÑA-Z] — ')

ALL_COLS = [
    'IA_Inteligencia_Artificial', 'Psicologia_Aplicada', 'Emprendimiento',
    'Salud_Bienestar', 'Finanzas_Personales', 'Productividad_Exito',
    'Relaciones_Comunicacion',
    'AI_Artificial_Intelligence', 'Applied_Psychology', 'Entrepreneurship',
    'Health_Wellness', 'Personal_Finance', 'Productivity_Success',
    'Relationships_Communication',
]


def patch_text(text):
    lines = text.splitlines(keepends=True)
    result = []
    changed = False
    for i, line in enumerate(lines):
        result.append(line)
        # If current line is an acronym line AND next line is also one (no blank between)
        if (RE_ACRO.match(line)
                and i + 1 < len(lines)
                and RE_ACRO.match(lines[i + 1])):
            result.append('\n')  # insert blank line
            changed = True
    return ''.join(result), changed


def patch_file(path):
    with open(path, encoding='utf-8-sig') as f:
        text = f.read()
    new_text, changed = patch_text(text)
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_text)
    return changed


total = changed = 0
for col in ALL_COLS:
    col_changed = 0
    for root, _, files in os.walk(os.path.join(BASE, col)):
        for fname in sorted(files):
            if not fname.endswith('.md') or fname == 'INDICE_MAESTRO.md':
                continue
            path = os.path.join(root, fname)
            total += 1
            if patch_file(path):
                col_changed += 1
                changed += 1
    if col_changed:
        print(f'  {col}: {col_changed} modificados')

print(f'\nTotal: {changed} / {total} archivos modificados')
