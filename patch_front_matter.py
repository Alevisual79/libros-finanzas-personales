"""
Reorganiza el front matter de los 1414 libros para que las páginas 3 y 4
queden en una sola pantalla Kindle.

ANTES (desborda):
  # Título          ← página 2
  ## Subtítulo      ← página 3 (h2 page-break)
  **Serie**
  ---
  *Copyright*
  ---
  > Aviso legal
  ---
  ### Prólogo       ← sin page-break, pero desborda a página 4
  [texto prólogo]

DESPUÉS (compacto):
  # Título          ← página 2
  **Serie**
  *Copyright*
  > Aviso legal
  ## Subtítulo      ← página 3 (h2 page-break)
  ### Prólogo       ← cabe en misma pantalla que subtítulo
  [texto prólogo]
"""
import os, re

BASE = r'c:\Users\usuario\Desktop\IA\Libros'

ALL_COLS = [
    'IA_Inteligencia_Artificial', 'Psicologia_Aplicada', 'Emprendimiento',
    'Salud_Bienestar', 'Finanzas_Personales', 'Productividad_Exito',
    'Relaciones_Comunicacion',
    'AI_Artificial_Intelligence', 'Applied_Psychology', 'Entrepreneurship',
    'Health_Wellness', 'Personal_Finance', 'Productivity_Success',
    'Relationships_Communication',
]

# Patrón flexible:
#  - Línea en blanco opcional entre h1 y h2
#  - 1 o más líneas **negrita** antes del copyright
#  - Captura todo el bloque hasta el último --- antes de ### Prólogo
RE_FRONT = re.compile(
    r'^(# [^\n]+)\n'                     # g1: h1 título
    r'\n?'                               # línea en blanco opcional (Salud, etc.)
    r'(## [^\n]+)\n\n'                   # g2: h2 subtítulo + blank
    r'((?:.*\n)*?)'                      # g3: todo el bloque (non-greedy, línea a línea)
    r'---\n\n'                           # último --- antes del Prólogo
    r'(### (?:Prólogo|Prologue)[^\n]*)', # g4: ### Prólogo[: subtítulo]
    re.MULTILINE
)


def repl(m):
    h1    = m.group(1)          # # Título
    h2    = m.group(2)          # ## Subtítulo
    block = m.group(3).rstrip() # todo el bloque entre h2 y ### Prólogo (sin trailing ---)
    prolog = m.group(4)         # ### Prólogo[: ...]
    # Nueva estructura: bloque copyright en página del título (h1), subtítulo + prólogo en página 3
    return (
        f'{h1}\n\n'
        f'{block}\n\n'
        f'{h2}\n\n'
        f'{prolog}'
    )


def patch_file(path):
    with open(path, encoding='utf-8-sig') as f:
        text = f.read()
    new_text = RE_FRONT.sub(repl, text)
    if new_text != text:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_text)
        return True
    return False


total = changed = 0
skipped = []
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
            else:
                skipped.append(f'{col}/{fname}')
    print(f'  {col}: {col_changed} modificados')

print(f'\nTotal: {changed} / {total} modificados')
if skipped:
    print(f'\nSIN CAMBIAR ({len(skipped)}):')
    for s in skipped[:20]:
        print(f'  {s}')
