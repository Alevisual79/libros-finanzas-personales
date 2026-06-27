"""
fix_spelling_v2.py — Correcciones ortográficas masivas (solo libros ES)
Corrige:
  1. modeló → modelo cuando es sustantivo (precedido de artículo/determinante)
  2. Preguntas sin ¿ (después de : y después de ?)
  3. Verbos condicionales sin tilde: habria/tendria/podria/deberia/vendria
  4. Imperfecto plural sin tilde: tenian/habian/sabian/podian/veian/etc.
  5. Errores de codificación ñ: Aniadir→Añadir, nino→niño, nina→niña
"""

import os, re

BASE = r"c:\Users\usuario\Desktop\IA\Libros"

ES_COLS = [
    "IA_Inteligencia_Artificial", "Psicologia_Aplicada", "Emprendimiento",
    "Salud_Bienestar", "Finanzas_Personales", "Productividad_Exito", "Relaciones_Comunicacion",
]

# ── Reglas de sustitución ────────────────────────────────────────────────────

# 1. modeló (sustantivo) precedido de artículo/determinante → modelo
RE_MODELO = re.compile(
    r'\b(el|un|del|este|ese|dicho|nuevo|mismo|propio|su|nuestro|los|estos|sus|cada|otro|'
    r'mi|tu|al|ningún|algún|cualquier|primer|segundo|tercer|cuarto|aquel|todo|cierto|este)\s+'
    r'(modeló)\b',
    re.IGNORECASE
)

def fix_modelo(line):
    return RE_MODELO.sub(lambda m: m.group(1) + ' modelo', line)


# 2a. Preguntas sin ¿ después de ':'
RE_Q_COLON = re.compile(r'(:\s+)(?!¿)([^:?!\n¿]{4,}\?)')

def fix_q_colon(line):
    def repl(m):
        text = m.group(2)
        if '¿' in text:
            return m.group(0)
        return m.group(1) + '¿' + text
    return RE_Q_COLON.sub(repl, line)


# 2b. Preguntas sin ¿ después de '? '
RE_Q_AFTER_Q = re.compile(r'(\?\s+)(?!¿)([A-ZÁÉÍÓÚÜÑ][^?!\n¿]{4,}\?)')

def fix_q_afterq(line):
    def repl(m):
        text = m.group(2)
        if '¿' in text:
            return m.group(0)
        return m.group(1) + '¿' + text
    return RE_Q_AFTER_Q.sub(repl, line)


# 2c. Preguntas sin ¿ después de '. ' cuando empieza con interrogativo conocido
# Acepta formas con y sin tilde (que/qué, como/cómo, etc.)
_INTERROG = (
    r'[Qq]u[eé]\s|[Cc][oó]mo\s|[Cc]u[aá]l(?:es)?\s|[Cc]u[aá]ndo\s|'
    r'[Qq]u[ií][eé]n(?:es)?\s|[Dd][oó]nde\s|[Cc]u[aá]nt[oa]s?\s|'
    r'[Pp]or\s+qu[eé]\s|[Pp]ara\s+qu[eé]\s'
)
RE_Q_AFTER_DOT = re.compile(
    rf'(\.\s+)(?!¿)((?:{_INTERROG})[^?!\n¿]{{2,}}\?)'
)

def fix_q_after_dot(line):
    def repl(m):
        text = m.group(2)
        if '¿' in text:
            return m.group(0)
        return m.group(1) + '¿' + text
    return RE_Q_AFTER_DOT.sub(repl, line)


# 3. Verbos condicionales sin tilde (solo formas claramente incorrectas)
COND_FIXES = [
    # habr-
    (re.compile(r'\bhabria\b', re.IGNORECASE),   'habría'),
    (re.compile(r'\bhabrias\b', re.IGNORECASE),  'habrías'),
    (re.compile(r'\bhabrian\b', re.IGNORECASE),  'habrían'),
    # tendr-
    (re.compile(r'\btendria\b', re.IGNORECASE),  'tendría'),
    (re.compile(r'\btendrias\b', re.IGNORECASE), 'tendrías'),
    (re.compile(r'\btendrian\b', re.IGNORECASE), 'tendrían'),
    # podr-
    (re.compile(r'\bpodria\b', re.IGNORECASE),   'podría'),
    (re.compile(r'\bpodrias\b', re.IGNORECASE),  'podrías'),
    (re.compile(r'\bpodrian\b', re.IGNORECASE),  'podrían'),
    # deber-
    (re.compile(r'\bdeberia\b', re.IGNORECASE),  'debería'),
    (re.compile(r'\bdeberias\b', re.IGNORECASE), 'deberías'),
    (re.compile(r'\bdeberian\b', re.IGNORECASE), 'deberían'),
    # vendr-
    (re.compile(r'\bvendria\b', re.IGNORECASE),  'vendría'),
    (re.compile(r'\bvendrias\b', re.IGNORECASE), 'vendrías'),
    (re.compile(r'\bvendrian\b', re.IGNORECASE), 'vendrían'),
    # querr-
    (re.compile(r'\bqueria\b', re.IGNORECASE),   'quería'),
    (re.compile(r'\bquerias\b', re.IGNORECASE),  'querías'),
    (re.compile(r'\bquerian\b', re.IGNORECASE),  'querían'),
    # sabr-
    (re.compile(r'\bsabria\b', re.IGNORECASE),   'sabría'),
    (re.compile(r'\bsabrias\b', re.IGNORECASE),  'sabrías'),
    (re.compile(r'\bsabrian\b', re.IGNORECASE),  'sabrían'),
]

def fix_conditional(line):
    for pattern, repl in COND_FIXES:
        # Preserve original case of first letter if was uppercase
        def _repl(m, r=repl):
            orig = m.group(0)
            if orig[0].isupper():
                return r[0].upper() + r[1:]
            return r
        line = pattern.sub(_repl, line)
    return line


# 4. Imperfecto plural sin tilde (3ª persona plural terminados en -ian/-ían)
IMPERF_FIXES = [
    (re.compile(r'\btenian\b', re.IGNORECASE),    'tenían'),
    (re.compile(r'\bhabian\b', re.IGNORECASE),    'habían'),
    (re.compile(r'\bsabian\b', re.IGNORECASE),    'sabían'),
    (re.compile(r'\bpodian\b', re.IGNORECASE),    'podían'),
    (re.compile(r'\bveian\b', re.IGNORECASE),     'veían'),
    (re.compile(r'\bdecian\b', re.IGNORECASE),    'decían'),
    (re.compile(r'\bvivian\b', re.IGNORECASE),    'vivían'),
    (re.compile(r'\bexistian\b', re.IGNORECASE),  'existían'),
    (re.compile(r'\bseguian\b', re.IGNORECASE),   'seguían'),
    (re.compile(r'\bsentian\b', re.IGNORECASE),   'sentían'),
    (re.compile(r'\bquerian\b', re.IGNORECASE),   'querían'),
    (re.compile(r'\bcreian\b', re.IGNORECASE),    'creían'),
    (re.compile(r'\bvolvian\b', re.IGNORECASE),   'volvían'),
    (re.compile(r'\bdormian\b', re.IGNORECASE),   'dormían'),
    (re.compile(r'\btraian\b', re.IGNORECASE),    'traían'),
    (re.compile(r'\bleian\b', re.IGNORECASE),     'leían'),
    (re.compile(r'\bescribian\b', re.IGNORECASE), 'escribían'),
    (re.compile(r'\bpedian\b', re.IGNORECASE),    'pedían'),
    (re.compile(r'\bvolvian\b', re.IGNORECASE),   'volvían'),
    # 2ª persona singular imperfecto (sin tilde)
    (re.compile(r'\bcreias\b', re.IGNORECASE),    'creías'),
    (re.compile(r'\btenias\b', re.IGNORECASE),    'tenías'),
    (re.compile(r'\bsabias\b', re.IGNORECASE),    'sabías'),
    (re.compile(r'\bpodias\b', re.IGNORECASE),    'podías'),
    (re.compile(r'\bveias\b', re.IGNORECASE),     'veías'),
    (re.compile(r'\bdeciais\b', re.IGNORECASE),   'decíais'),
]

# 4b. Imperativos reflexivos sin tilde
IMPER_FIXES = [
    (re.compile(r'\bpreguntate\b',   re.IGNORECASE), 'pregúntate'),
    (re.compile(r'\bcomprometete\b', re.IGNORECASE), 'comprométete'),
    (re.compile(r'\blevantate\b',    re.IGNORECASE), 'levántate'),
    (re.compile(r'\bdedicate\b',     re.IGNORECASE), 'dedícate'),
    (re.compile(r'\bfijate\b',       re.IGNORECASE), 'fíjate'),
    (re.compile(r'\benfocate\b',     re.IGNORECASE), 'enfócate'),
    (re.compile(r'\brecuerdate\b',   re.IGNORECASE), 'recuérdate'),
    (re.compile(r'\batrevete\b',     re.IGNORECASE), 'atrévete'),
    (re.compile(r'\bpermitete\b',    re.IGNORECASE), 'permítete'),
    (re.compile(r'\bmuevete\b',      re.IGNORECASE), 'muévete'),
    (re.compile(r'\bimaginate\b',    re.IGNORECASE), 'imagínate'),
    (re.compile(r'\bcomunicate\b',   re.IGNORECASE), 'comunícate'),
    (re.compile(r'\bescuchate\b',    re.IGNORECASE), 'escúchate'),
    (re.compile(r'\bobservate\b',    re.IGNORECASE), 'obsérvate'),
    (re.compile(r'\bquedate\b',      re.IGNORECASE), 'quédate'),
    (re.compile(r'\bmuestrate\b',    re.IGNORECASE), 'muéstrate'),
    (re.compile(r'\btomate\b',       re.IGNORECASE), 'tómate'),
    (re.compile(r'\banotalo\b',      re.IGNORECASE), 'anótalo'),
    (re.compile(r'\bpruebalo\b',     re.IGNORECASE), 'pruébalo'),
    (re.compile(r'\bescribelo\b',    re.IGNORECASE), 'escríbelo'),
    (re.compile(r'\bpiensalo\b',     re.IGNORECASE), 'piénsalo'),
    (re.compile(r'\bdejate\b',       re.IGNORECASE), 'déjate'),
    (re.compile(r'\bcuidate\b',      re.IGNORECASE), 'cuídate'),
    (re.compile(r'\bacuerdate\b',    re.IGNORECASE), 'acuérdate'),
    (re.compile(r'\bconviertete\b',  re.IGNORECASE), 'conviértete'),
]

def fix_imperfect(line):
    for pattern, repl in IMPERF_FIXES:
        def _repl(m, r=repl):
            orig = m.group(0)
            if orig[0].isupper():
                return r[0].upper() + r[1:]
            return r
        line = pattern.sub(_repl, line)
    return line

def fix_imperatives(line):
    for pattern, repl in IMPER_FIXES:
        def _repl(m, r=repl):
            orig = m.group(0)
            if orig[0].isupper():
                return r[0].upper() + r[1:]
            return r
        line = pattern.sub(_repl, line)
    return line


# 5. Errores de codificación ñ
ENCOD_FIXES = [
    (re.compile(r'\bAniadir\b'),    'Añadir'),
    (re.compile(r'\baniadir\b'),    'añadir'),
    (re.compile(r'\bnino\b'),       'niño'),
    (re.compile(r'\bninos\b'),      'niños'),
    (re.compile(r'\bnina\b'),       'niña'),
    (re.compile(r'\bninas\b'),      'niñas'),
    (re.compile(r'\bNino\b'),       'Niño'),
    (re.compile(r'\bNinos\b'),      'Niños'),
    (re.compile(r'\bNina\b'),       'Niña'),
    (re.compile(r'\bNinas\b'),      'Niñas'),
]

def fix_encoding(line):
    for pattern, repl in ENCOD_FIXES:
        line = pattern.sub(repl, line)
    return line


# ── Procesado por línea ──────────────────────────────────────────────────────

def fix_line(line):
    stripped = line.strip()
    # Conservar líneas vacías, encabezados, citas, tablas, código
    if not stripped:
        return line
    if stripped.startswith(('#', '`', '|')):
        return line
    # Blockquotes (disclaimer/aviso legal) — no tocar
    if stripped.startswith('>'):
        return line

    line = fix_encoding(line)
    line = fix_modelo(line)
    line = fix_conditional(line)
    line = fix_imperfect(line)
    line = fix_imperatives(line)
    line = fix_q_colon(line)
    line = fix_q_afterq(line)
    line = fix_q_after_dot(line)
    return line


def fix_file(path):
    with open(path, encoding='utf-8-sig') as f:
        original = f.read()

    lines = original.split('\n')
    new_lines = [fix_line(l) for l in lines]
    new_text = '\n'.join(new_lines)

    if new_text != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_text)
        return True
    return False


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    total_files = 0
    modified = 0

    for col in ES_COLS:
        col_path = os.path.join(BASE, col)
        col_modified = 0
        for root, _, files in os.walk(col_path):
            for fname in sorted(files):
                if not fname.endswith('.md'):
                    continue
                path = os.path.join(root, fname)
                total_files += 1
                if fix_file(path):
                    col_modified += 1
                    modified += 1
        print(f"  {col}: {col_modified} archivos modificados")

    print(f"\nTotal: {modified} / {total_files} archivos ES modificados")


if __name__ == '__main__':
    main()
