"""
Dos cambios en todos los libros (1414 .md):
1. ## Prólogo / ## Prologue → ### (sin page-break-before, = páginas 3+4 en una)
2. Actualizar texto de "Sobre el Autor" / "About the Author"
"""
import os, re

BASE = r'c:\Users\usuario\Desktop\IA\Libros'

ES_COLS = [
    'IA_Inteligencia_Artificial', 'Psicologia_Aplicada', 'Emprendimiento',
    'Salud_Bienestar', 'Finanzas_Personales', 'Productividad_Exito',
    'Relaciones_Comunicacion',
]
EN_COLS = [
    'AI_Artificial_Intelligence', 'Applied_Psychology', 'Entrepreneurship',
    'Health_Wellness', 'Personal_Finance', 'Productivity_Success',
    'Relationships_Communication',
]

# ── ES bio: solo cambia coma por punto entre las dos frases ──────────────────
ES_BIO_OLD = (
    'las personas no fracasan por falta de información. '
    'Fracasan porque nadie les dio las herramientas correctas en el momento exacto.'
)
ES_BIO_NEW = (
    'las personas no fracasan por falta de información, '
    'fracasan porque nadie les dio las herramientas correctas en el momento exacto.'
)

# ── EN bio: alinear con nueva versión ES ─────────────────────────────────────
EN_BIO_OLD = (
    'Twenty-five years across different companies taught him something few dare to say out loud: '
    "people don't fail because they lack information. "
    "They fail because nobody gave them the right tools at the right moment. "
    "This collection exists to change that. "
    "Each book distills what truly works — no filler, no empty theory. "
    "Developed with the support of artificial intelligence to carry that knowledge "
    "further than any single author could reach alone."
)
EN_BIO_NEW = (
    'Twenty-five years across different companies taught him something few dare to say: '
    "people don't fail because they lack information, "
    "they fail because nobody gave them the right tools at the right moment. "
    "This collection exists to change that. "
    "Each book distills what truly works, no filler, no empty theory. "
    "Developed with the support of artificial intelligence to carry that knowledge "
    "further than any author could reach alone."
)

RE_ES_PROLOG = re.compile(r'^## Prólogo\s*$', re.MULTILINE)
RE_EN_PROLOG = re.compile(r'^## Prologue\s*$', re.MULTILINE)


def patch_file(path, is_es):
    with open(path, encoding='utf-8-sig') as f:
        text = f.read()

    original = text

    if is_es:
        # 1. ## Prólogo → ### Prólogo
        text = RE_ES_PROLOG.sub('### Prólogo', text)
        # 2. Bio ES
        text = text.replace(ES_BIO_OLD, ES_BIO_NEW)
    else:
        # 1. ## Prologue → ### Prologue
        text = RE_EN_PROLOG.sub('### Prologue', text)
        # 2. Bio EN
        text = text.replace(EN_BIO_OLD, EN_BIO_NEW)

    if text != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    return False


total = 0
for cols, is_es in [(ES_COLS, True), (EN_COLS, False)]:
    for col in cols:
        modified = 0
        col_path = os.path.join(BASE, col)
        for root, _, files in os.walk(col_path):
            for fname in files:
                if not fname.endswith('.md'):
                    continue
                if patch_file(os.path.join(root, fname), is_es):
                    modified += 1
        lang = 'ES' if is_es else 'EN'
        print(f'  [{lang}] {col}: {modified} archivos modificados')
        total += modified

print(f'\nTotal: {total} / 1414 archivos modificados')
