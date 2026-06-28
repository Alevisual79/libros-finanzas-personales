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
    # 'tomate' EXCLUIDO — es el vegetal en libros de salud/cocina
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


# 5. 'esta' → 'está' (verbo estar sin tilde)
# General: esta + cualquier participio regular (-ado/-ido) o gerundio
# 'estado' excluido: es sustantivo masculino (diría 'este estado', no 'esta estado')
RE_ESTA_PART  = re.compile(r'\besta\s+\w+[ai]do\b', re.IGNORECASE)
RE_ESTA_GER   = re.compile(r'\besta\s+\w+(?:ando|endo|iendo|yendo)\b', re.IGNORECASE)
RE_ESTA_PUNTO = re.compile(r'\besta\s+a\s+punto\b', re.IGNORECASE)
RE_ESTA_MISC  = re.compile(r'\besta\s+(?:bien|claro|lista?|disponible|muy\b)', re.IGNORECASE)

def _repl_esta(m):
    s = m.group(0)
    prefix = 'Está ' if s[0].isupper() else 'está '
    return prefix + s.split(None, 1)[1]

def fix_esta(line):
    line = RE_ESTA_PART.sub(_repl_esta, line)
    line = RE_ESTA_GER.sub(_repl_esta, line)
    line = RE_ESTA_PUNTO.sub(_repl_esta, line)
    line = RE_ESTA_MISC.sub(_repl_esta, line)
    return line


# 6. Errores de codificación ñ
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


# 7. Adjetivos/sustantivos sin tilde (esdrújulas — siempre llevan tilde)
# Safe: only words that cannot be verb forms (no ambiguity)
ESDRUJ_FIXES = [
    # académic*
    (re.compile(r'\bacademica\b',     re.IGNORECASE), 'académica'),
    (re.compile(r'\bacademico\b',     re.IGNORECASE), 'académico'),
    (re.compile(r'\bacademicas\b',    re.IGNORECASE), 'académicas'),
    (re.compile(r'\bacademicos\b',    re.IGNORECASE), 'académicos'),
    # económic*
    (re.compile(r'\beconomica\b',     re.IGNORECASE), 'económica'),
    (re.compile(r'\beconomico\b',     re.IGNORECASE), 'económico'),
    (re.compile(r'\beconomicas\b',    re.IGNORECASE), 'económicas'),
    (re.compile(r'\beconomicos\b',    re.IGNORECASE), 'económicos'),
    # técnic*
    (re.compile(r'\btecnica\b',       re.IGNORECASE), 'técnica'),
    (re.compile(r'\btecnico\b',       re.IGNORECASE), 'técnico'),
    (re.compile(r'\btecnicas\b',      re.IGNORECASE), 'técnicas'),
    (re.compile(r'\btecnicos\b',      re.IGNORECASE), 'técnicos'),
    # característic*
    (re.compile(r'\bcaracteristica\b',  re.IGNORECASE), 'característica'),
    (re.compile(r'\bcaracteristico\b',  re.IGNORECASE), 'característico'),
    (re.compile(r'\bcaracteristicas\b', re.IGNORECASE), 'características'),
    (re.compile(r'\bcaracteristicos\b', re.IGNORECASE), 'característicos'),
    # lógic*
    (re.compile(r'\blogica\b',        re.IGNORECASE), 'lógica'),
    (re.compile(r'\blogico\b',        re.IGNORECASE), 'lógico'),
    (re.compile(r'\blogicas\b',       re.IGNORECASE), 'lógicas'),
    (re.compile(r'\blogicos\b',       re.IGNORECASE), 'lógicos'),
    # código (noun; "yo codifico" is different)
    (re.compile(r'\bcodigo\b',        re.IGNORECASE), 'código'),
    (re.compile(r'\bcodigos\b',       re.IGNORECASE), 'códigos'),
    # orgánic*
    (re.compile(r'\borganica\b',      re.IGNORECASE), 'orgánica'),
    (re.compile(r'\borganico\b',      re.IGNORECASE), 'orgánico'),
    (re.compile(r'\borganicas\b',     re.IGNORECASE), 'orgánicas'),
    (re.compile(r'\borganicos\b',     re.IGNORECASE), 'orgánicos'),
    # diagnóstic*
    (re.compile(r'\bdiagnostico\b',   re.IGNORECASE), 'diagnóstico'),
    (re.compile(r'\bdiagnosticos\b',  re.IGNORECASE), 'diagnósticos'),
    # fisiológic*
    (re.compile(r'\bfisiologica\b',   re.IGNORECASE), 'fisiológica'),
    (re.compile(r'\bfisiologico\b',   re.IGNORECASE), 'fisiológico'),
    (re.compile(r'\bfisiologicas\b',  re.IGNORECASE), 'fisiológicas'),
    (re.compile(r'\bfisiologicos\b',  re.IGNORECASE), 'fisiológicos'),
    # psicológic*
    (re.compile(r'\bpsicologica\b',   re.IGNORECASE), 'psicológica'),
    (re.compile(r'\bpsicologico\b',   re.IGNORECASE), 'psicológico'),
    (re.compile(r'\bpsicologicas\b',  re.IGNORECASE), 'psicológicas'),
    (re.compile(r'\bpsicologicos\b',  re.IGNORECASE), 'psicológicos'),
    # biológic*
    (re.compile(r'\bbiologica\b',     re.IGNORECASE), 'biológica'),
    (re.compile(r'\bbiologico\b',     re.IGNORECASE), 'biológico'),
    (re.compile(r'\bbiologicas\b',    re.IGNORECASE), 'biológicas'),
    (re.compile(r'\bbiologicos\b',    re.IGNORECASE), 'biológicos'),
    # automátic*
    (re.compile(r'\bautomatica\b',    re.IGNORECASE), 'automática'),
    (re.compile(r'\bautomatico\b',    re.IGNORECASE), 'automático'),
    (re.compile(r'\bautomaticas\b',   re.IGNORECASE), 'automáticas'),
    (re.compile(r'\bautomaticos\b',   re.IGNORECASE), 'automáticos'),
    # históric*
    (re.compile(r'\bhistorica\b',     re.IGNORECASE), 'histórica'),
    (re.compile(r'\bhistorico\b',     re.IGNORECASE), 'histórico'),
    (re.compile(r'\bhistoricas\b',    re.IGNORECASE), 'históricas'),
    (re.compile(r'\bhistoricos\b',    re.IGNORECASE), 'históricos'),
    # estratégic*
    (re.compile(r'\bestrategica\b',   re.IGNORECASE), 'estratégica'),
    (re.compile(r'\bestrategico\b',   re.IGNORECASE), 'estratégico'),
    (re.compile(r'\bestrategicas\b',  re.IGNORECASE), 'estratégicas'),
    (re.compile(r'\bestrategicos\b',  re.IGNORECASE), 'estratégicos'),
    # sistemátic*
    (re.compile(r'\bsistematica\b',   re.IGNORECASE), 'sistemática'),
    (re.compile(r'\bsistematico\b',   re.IGNORECASE), 'sistemático'),
    (re.compile(r'\bsistematicas\b',  re.IGNORECASE), 'sistemáticas'),
    (re.compile(r'\bsistematicos\b',  re.IGNORECASE), 'sistemáticos'),
    # sintétic*
    (re.compile(r'\bsintetica\b',     re.IGNORECASE), 'sintética'),
    (re.compile(r'\bsintetico\b',     re.IGNORECASE), 'sintético'),
    (re.compile(r'\bsinteticas\b',    re.IGNORECASE), 'sintéticas'),
    (re.compile(r'\bsinteticos\b',    re.IGNORECASE), 'sintéticos'),
    # enérgic* / energétic*
    (re.compile(r'\benergetica\b',    re.IGNORECASE), 'energética'),
    (re.compile(r'\benergetico\b',    re.IGNORECASE), 'energético'),
    (re.compile(r'\benergeticas\b',   re.IGNORECASE), 'energéticas'),
    (re.compile(r'\benergeticos\b',   re.IGNORECASE), 'energéticos'),
    # crític* EXCLUIDO — 'critica/critico' también son formas verbales de "criticar"
    # farmacológic*
    (re.compile(r'\bfarmacologica\b', re.IGNORECASE), 'farmacológica'),
    (re.compile(r'\bfarmacologico\b', re.IGNORECASE), 'farmacológico'),
    (re.compile(r'\bfarmacologicas\b',re.IGNORECASE), 'farmacológicas'),
    (re.compile(r'\bfarmacologicos\b',re.IGNORECASE), 'farmacológicos'),
    # neurológic*
    (re.compile(r'\bneurologica\b',   re.IGNORECASE), 'neurológica'),
    (re.compile(r'\bneurologico\b',   re.IGNORECASE), 'neurológico'),
    (re.compile(r'\bneurologicas\b',  re.IGNORECASE), 'neurológicas'),
    (re.compile(r'\bneurologicos\b',  re.IGNORECASE), 'neurológicos'),
    # analógic*
    (re.compile(r'\banalogica\b',     re.IGNORECASE), 'analógica'),
    (re.compile(r'\banalogico\b',     re.IGNORECASE), 'analógico'),
    # matemátic*
    (re.compile(r'\bmatematica\b',    re.IGNORECASE), 'matemática'),
    (re.compile(r'\bmatematico\b',    re.IGNORECASE), 'matemático'),
    (re.compile(r'\bmatematicas\b',   re.IGNORECASE), 'matemáticas'),
    (re.compile(r'\bmatematicos\b',   re.IGNORECASE), 'matemáticos'),
    # fenómeno
    (re.compile(r'\bfenomeno\b',      re.IGNORECASE), 'fenómeno'),
    (re.compile(r'\bfenomenos\b',     re.IGNORECASE), 'fenómenos'),
    # análisis (invariable)
    (re.compile(r'\banalisis\b',      re.IGNORECASE), 'análisis'),
    # método/s
    (re.compile(r'\bmetodo\b',        re.IGNORECASE), 'método'),
    (re.compile(r'\bmetodos\b',       re.IGNORECASE), 'métodos'),
    # número/s
    (re.compile(r'\bnumero\b',        re.IGNORECASE), 'número'),
    (re.compile(r'\bnumeros\b',       re.IGNORECASE), 'números'),
    # teléfono/s
    (re.compile(r'\btelefono\b',      re.IGNORECASE), 'teléfono'),
    (re.compile(r'\btelefonos\b',     re.IGNORECASE), 'teléfonos'),
    # período/s
    (re.compile(r'\bperiodo\b',       re.IGNORECASE), 'período'),
    (re.compile(r'\bperiodos\b',      re.IGNORECASE), 'períodos'),
    # artículo/s
    (re.compile(r'\barticulo\b',      re.IGNORECASE), 'artículo'),
    (re.compile(r'\barticulos\b',     re.IGNORECASE), 'artículos'),
    # último/s/a/as
    (re.compile(r'\bultimo\b',        re.IGNORECASE), 'último'),
    (re.compile(r'\bultima\b',        re.IGNORECASE), 'última'),
    (re.compile(r'\bultimos\b',       re.IGNORECASE), 'últimos'),
    (re.compile(r'\bultimas\b',       re.IGNORECASE), 'últimas'),
    # próximo/s/a/as
    (re.compile(r'\bproximo\b',       re.IGNORECASE), 'próximo'),
    (re.compile(r'\bproxima\b',       re.IGNORECASE), 'próxima'),
    (re.compile(r'\bproximos\b',      re.IGNORECASE), 'próximos'),
    (re.compile(r'\bproximas\b',      re.IGNORECASE), 'próximas'),
    # dinámico/s/a/as
    (re.compile(r'\bdinamica\b',      re.IGNORECASE), 'dinámica'),
    (re.compile(r'\bdinamico\b',      re.IGNORECASE), 'dinámico'),
    (re.compile(r'\bdinamicas\b',     re.IGNORECASE), 'dinámicas'),
    (re.compile(r'\bdinamicos\b',     re.IGNORECASE), 'dinámicos'),
    # físic* (careful: fisico/fisica as adj for subject "physical"; not verb)
    (re.compile(r'\bfisica\b',        re.IGNORECASE), 'física'),
    (re.compile(r'\bfisico\b',        re.IGNORECASE), 'físico'),
    (re.compile(r'\bfisicas\b',       re.IGNORECASE), 'físicas'),
    (re.compile(r'\bfisicos\b',       re.IGNORECASE), 'físicos'),
    # hábito/s (very common in psychology/productivity books)
    (re.compile(r'\bhabito\b',        re.IGNORECASE), 'hábito'),
    (re.compile(r'\bhabitos\b',       re.IGNORECASE), 'hábitos'),
    # búsqueda/s (common in AI/research books)
    (re.compile(r'\bbusqueda\b',      re.IGNORECASE), 'búsqueda'),
    (re.compile(r'\bbusquedas\b',     re.IGNORECASE), 'búsquedas'),
    # metodología/s
    (re.compile(r'\bmetodologia\b',   re.IGNORECASE), 'metodología'),
    (re.compile(r'\bmetodologias\b',  re.IGNORECASE), 'metodologías'),
    # ingeniería
    (re.compile(r'\bingenieria\b',    re.IGNORECASE), 'ingeniería'),
    # estrés (invariable)
    (re.compile(r'\bestres\b',        re.IGNORECASE), 'estrés'),
    # síndrome/s
    (re.compile(r'\bsindrome\b',      re.IGNORECASE), 'síndrome'),
    (re.compile(r'\bsindromes\b',     re.IGNORECASE), 'síndromes'),
    # específic*
    (re.compile(r'\bespecifica\b',    re.IGNORECASE), 'específica'),
    (re.compile(r'\bespecifico\b',    re.IGNORECASE), 'específico'),
    (re.compile(r'\bespecificas\b',   re.IGNORECASE), 'específicas'),
    (re.compile(r'\bespecificos\b',   re.IGNORECASE), 'específicos'),
    (re.compile(r'\bespecificamente\b', re.IGNORECASE), 'específicamente'),
    # terapéutic*
    (re.compile(r'\bterapeutica\b',   re.IGNORECASE), 'terapéutica'),
    (re.compile(r'\bterapeutico\b',   re.IGNORECASE), 'terapéutico'),
    (re.compile(r'\bterapeuticas\b',  re.IGNORECASE), 'terapéuticas'),
    (re.compile(r'\bterapeuticos\b',  re.IGNORECASE), 'terapéuticos'),
    # traumátic*
    (re.compile(r'\btraumatica\b',    re.IGNORECASE), 'traumática'),
    (re.compile(r'\btraumatico\b',    re.IGNORECASE), 'traumático'),
    (re.compile(r'\btraumaticas\b',   re.IGNORECASE), 'traumáticas'),
    (re.compile(r'\btraumaticos\b',   re.IGNORECASE), 'traumáticos'),
    # prácticamente
    (re.compile(r'\bpracticamente\b', re.IGNORECASE), 'prácticamente'),
    # electrónic*
    (re.compile(r'\belectronica\b',   re.IGNORECASE), 'electrónica'),
    (re.compile(r'\belectronico\b',   re.IGNORECASE), 'electrónico'),
    (re.compile(r'\belectronicas\b',  re.IGNORECASE), 'electrónicas'),
    (re.compile(r'\belectronicos\b',  re.IGNORECASE), 'electrónicos'),
    # página/s
    (re.compile(r'\bpagina\b',        re.IGNORECASE), 'página'),
    (re.compile(r'\bpaginas\b',       re.IGNORECASE), 'páginas'),
    # orgán(o) — careful: órgano vs organización
    (re.compile(r'\borgano\b',        re.IGNORECASE), 'órgano'),
    (re.compile(r'\borganos\b',       re.IGNORECASE), 'órganos'),
    # síntesis
    (re.compile(r'\bsintesis\b',      re.IGNORECASE), 'síntesis'),
    # hipótesis
    (re.compile(r'\bhipotesis\b',     re.IGNORECASE), 'hipótesis'),
    # énfasis
    (re.compile(r'\benfasis\b',       re.IGNORECASE), 'énfasis'),
    # ámbito/s
    (re.compile(r'\bambito\b',        re.IGNORECASE), 'ámbito'),
    (re.compile(r'\bambitos\b',       re.IGNORECASE), 'ámbitos'),
    # índice/s
    (re.compile(r'\bindice\b',        re.IGNORECASE), 'índice'),
    (re.compile(r'\bindices\b',       re.IGNORECASE), 'índices'),
    # víncul*
    (re.compile(r'\bvinculo\b',       re.IGNORECASE), 'vínculo'),
    (re.compile(r'\bvinculos\b',      re.IGNORECASE), 'vínculos'),
    # músculo/s
    (re.compile(r'\bmusculo\b',       re.IGNORECASE), 'músculo'),
    (re.compile(r'\bmusculos\b',      re.IGNORECASE), 'músculos'),
    # cronológic*
    (re.compile(r'\bcronologica\b',   re.IGNORECASE), 'cronológica'),
    (re.compile(r'\bcronologico\b',   re.IGNORECASE), 'cronológico'),
    # genétic*
    (re.compile(r'\bgenetica\b',      re.IGNORECASE), 'genética'),
    (re.compile(r'\bgenetico\b',      re.IGNORECASE), 'genético'),
    (re.compile(r'\bgeneticas\b',     re.IGNORECASE), 'genéticas'),
    (re.compile(r'\bgeneticos\b',     re.IGNORECASE), 'genéticos'),
    # metabólic*
    (re.compile(r'\bmetabolica\b',    re.IGNORECASE), 'metabólica'),
    (re.compile(r'\bmetabolico\b',    re.IGNORECASE), 'metabólico'),
    (re.compile(r'\bmetabolicas\b',   re.IGNORECASE), 'metabólicas'),
    (re.compile(r'\bmetabolicos\b',   re.IGNORECASE), 'metabólicos'),
    # epidemiológic*
    (re.compile(r'\bepidemiologica\b',re.IGNORECASE), 'epidemiológica'),
    (re.compile(r'\bepidemiologico\b',re.IGNORECASE), 'epidemiológico'),
    # estadístic*
    (re.compile(r'\bestadistica\b',   re.IGNORECASE), 'estadística'),
    (re.compile(r'\bestadistico\b',   re.IGNORECASE), 'estadístico'),
    (re.compile(r'\bestadisticas\b',  re.IGNORECASE), 'estadísticas'),
    (re.compile(r'\bestadisticos\b',  re.IGNORECASE), 'estadísticos'),
    # democrátic*
    (re.compile(r'\bdemocratica\b',   re.IGNORECASE), 'democrática'),
    (re.compile(r'\bdemocratico\b',   re.IGNORECASE), 'democrático'),
    # neurocientífic*
    (re.compile(r'\bneurocientifico\b', re.IGNORECASE), 'neurocientífico'),
    (re.compile(r'\bneurocientifica\b', re.IGNORECASE), 'neurocientífica'),
    # clásic*
    (re.compile(r'\bclasica\b',       re.IGNORECASE), 'clásica'),
    (re.compile(r'\bclasico\b',       re.IGNORECASE), 'clásico'),
    (re.compile(r'\bclasicas\b',      re.IGNORECASE), 'clásicas'),
    (re.compile(r'\bclasicos\b',      re.IGNORECASE), 'clásicos'),
    # típic*
    (re.compile(r'\btipica\b',        re.IGNORECASE), 'típica'),
    (re.compile(r'\btipico\b',        re.IGNORECASE), 'típico'),
    (re.compile(r'\btipicas\b',       re.IGNORECASE), 'típicas'),
    (re.compile(r'\btipicos\b',       re.IGNORECASE), 'típicos'),
    # narraciones (singular: narración — but these singulars missing accent)
    (re.compile(r'\bnarracion\b',     re.IGNORECASE), 'narración'),
    # situación (singular only — plural 'situaciones' is correct)
    (re.compile(r'\bsituacion\b',     re.IGNORECASE), 'situación'),
    # relación (singular only)
    (re.compile(r'\brelacion\b',      re.IGNORECASE), 'relación'),
    # información (singular only)
    (re.compile(r'\binformacion\b',   re.IGNORECASE), 'información'),
    # comunicación (singular only)
    (re.compile(r'\bcomunicacion\b',  re.IGNORECASE), 'comunicación'),
    # decisión (singular only)
    (re.compile(r'\bdecision\b',      re.IGNORECASE), 'decisión'),
    # solución (singular only)
    (re.compile(r'\bsolucion\b',      re.IGNORECASE), 'solución'),
    # función (singular only)
    (re.compile(r'\bfuncion\b',       re.IGNORECASE), 'función'),
    # presentación (singular only)
    (re.compile(r'\bpresentacion\b',  re.IGNORECASE), 'presentación'),
    # organización (singular only)
    (re.compile(r'\borganizacion\b',  re.IGNORECASE), 'organización'),
    # intervención (singular only)
    (re.compile(r'\bintervencion\b',  re.IGNORECASE), 'intervención'),
    # evaluación (singular only)
    (re.compile(r'\bevaluacion\b',    re.IGNORECASE), 'evaluación'),
    # investigación (singular only)
    (re.compile(r'\binvestigacion\b', re.IGNORECASE), 'investigación'),
    # generación (singular only)
    (re.compile(r'\bgeneracion\b',    re.IGNORECASE), 'generación'),
    # atención (singular only)
    (re.compile(r'\batencion\b',      re.IGNORECASE), 'atención'),
    # introducción (singular only)
    (re.compile(r'\bintroduccion\b',  re.IGNORECASE), 'introducción'),
    # creación (singular only)
    (re.compile(r'\bcreacion\b',      re.IGNORECASE), 'creación'),
    # producción (singular only)
    (re.compile(r'\bproduccion\b',    re.IGNORECASE), 'producción'),
    # protección (singular only)
    (re.compile(r'\bproteccion\b',    re.IGNORECASE), 'protección'),
    # percepción (singular only)
    (re.compile(r'\bpercepcion\b',    re.IGNORECASE), 'percepción'),
    # concentración (singular only)
    (re.compile(r'\bconcentracion\b', re.IGNORECASE), 'concentración'),
    # dirección (singular only)
    (re.compile(r'\bdireccion\b',     re.IGNORECASE), 'dirección'),
    # posición (singular only)
    (re.compile(r'\bposicion\b',      re.IGNORECASE), 'posición'),
    # composición (singular only)
    (re.compile(r'\bcomposicion\b',   re.IGNORECASE), 'composición'),
    # distribución (singular only)
    (re.compile(r'\bdistribucion\b',  re.IGNORECASE), 'distribución'),
    # contribución (singular only)
    (re.compile(r'\bcontribucion\b',  re.IGNORECASE), 'contribución'),
    # conclusión (singular only)
    (re.compile(r'\bconclusion\b',    re.IGNORECASE), 'conclusión'),
    # publicación (singular only)
    (re.compile(r'\bpublicacion\b',   re.IGNORECASE), 'publicación'),
    # explicación (singular only)
    (re.compile(r'\bexplicacion\b',   re.IGNORECASE), 'explicación'),
    # implementación (singular only)
    (re.compile(r'\bimplementacion\b',re.IGNORECASE), 'implementación'),
    # institución (singular only)
    (re.compile(r'\binstitucion\b',   re.IGNORECASE), 'institución'),
    # población (singular only)
    (re.compile(r'\bpoblacion\b',     re.IGNORECASE), 'población'),
    # evolución (singular only)
    (re.compile(r'\bevolucion\b',     re.IGNORECASE), 'evolución'),
    # depresión (singular only)
    (re.compile(r'\bdepresion\b',     re.IGNORECASE), 'depresión'),
    # presión (singular only)
    (re.compile(r'\bpresion\b',       re.IGNORECASE), 'presión'),
    # prevención (singular only)
    (re.compile(r'\bprevencion\b',    re.IGNORECASE), 'prevención'),
    # afirmación (singular only)
    (re.compile(r'\bafirmacion\b',    re.IGNORECASE), 'afirmación'),
    # mención (singular only)
    (re.compile(r'\bmencion\b',       re.IGNORECASE), 'mención'),
    # educación (singular only)
    (re.compile(r'\beducacion\b',     re.IGNORECASE), 'educación'),
    # fundación (singular only)
    (re.compile(r'\bfundacion\b',     re.IGNORECASE), 'fundación'),
    # participación (singular only)
    (re.compile(r'\bparticipacion\b', re.IGNORECASE), 'participación'),
    # acción (singular only) — careful: 'accion' matches "acción"
    (re.compile(r'\baccion\b',        re.IGNORECASE), 'acción'),
    # reacción (singular only)
    (re.compile(r'\breaccion\b',      re.IGNORECASE), 'reacción'),
    # interacción (singular only)
    (re.compile(r'\binteraccion\b',   re.IGNORECASE), 'interacción'),
    # satisfacción (singular only)
    (re.compile(r'\bsatisfaccion\b',  re.IGNORECASE), 'satisfacción'),
    # adopción (singular only)
    (re.compile(r'\badopcion\b',      re.IGNORECASE), 'adopción'),
    # absorción (singular only)
    (re.compile(r'\babsorcion\b',     re.IGNORECASE), 'absorción'),
    # implicación (singular only)
    (re.compile(r'\bimplicacion\b',   re.IGNORECASE), 'implicación'),
    # habitación (singular only)
    (re.compile(r'\bhabitacion\b',    re.IGNORECASE), 'habitación'),
    # observación (singular only)
    (re.compile(r'\bobservacion\b',   re.IGNORECASE), 'observación'),
    # transformación (singular only)
    (re.compile(r'\btransformacion\b',re.IGNORECASE), 'transformación'),
    # confrontación (singular only)
    (re.compile(r'\bconfrontacion\b', re.IGNORECASE), 'confrontación'),
    # denominación (singular only)
    (re.compile(r'\bdenominacion\b',  re.IGNORECASE), 'denominación'),
    # conversación (singular only)
    (re.compile(r'\bconversacion\b',  re.IGNORECASE), 'conversación'),
    # aplicación (singular only)
    (re.compile(r'\baplicacion\b',    re.IGNORECASE), 'aplicación'),
    # recuperación (singular only)
    (re.compile(r'\brecuperacion\b',  re.IGNORECASE), 'recuperación'),
    # regulación (singular only)
    (re.compile(r'\bregulacion\b',    re.IGNORECASE), 'regulación'),
    # manipulación (singular only)
    (re.compile(r'\bmanipulacion\b',  re.IGNORECASE), 'manipulación'),
    # resolución (singular only)
    (re.compile(r'\bresolucion\b',    re.IGNORECASE), 'resolución'),
    # versión (singular only)
    (re.compile(r'\bversion\b',       re.IGNORECASE), 'versión'),
    # cuestión (singular only)
    (re.compile(r'\bcuestion\b',      re.IGNORECASE), 'cuestión'),
    # atracción (singular only)
    (re.compile(r'\batraccion\b',     re.IGNORECASE), 'atracción'),
    # inspiración (singular only)
    (re.compile(r'\binspiracion\b',   re.IGNORECASE), 'inspiración'),
    # motivación (singular only)
    (re.compile(r'\bmotivacion\b',    re.IGNORECASE), 'motivación'),
    # adaptación (singular only)
    (re.compile(r'\badaptacion\b',    re.IGNORECASE), 'adaptación'),
    # comprensión (singular only)
    (re.compile(r'\bcomprension\b',   re.IGNORECASE), 'comprensión'),
    # conexión (singular only)
    (re.compile(r'\bconexion\b',      re.IGNORECASE), 'conexión'),
    # dimensión (singular only)
    (re.compile(r'\bdimension\b',     re.IGNORECASE), 'dimensión'),
    # intención (singular only)
    (re.compile(r'\bintencion\b',     re.IGNORECASE), 'intención'),
    # tensión (singular only)
    (re.compile(r'\btension\b',       re.IGNORECASE), 'tensión'),
    # noción (singular only)
    (re.compile(r'\bnocion\b',        re.IGNORECASE), 'noción'),
    # selección (singular only)
    (re.compile(r'\bseleccion\b',     re.IGNORECASE), 'selección'),
    # recomendación (singular only)
    (re.compile(r'\brecomendacion\b', re.IGNORECASE), 'recomendación'),
    # dedicación (singular only)
    (re.compile(r'\bdedicacion\b',    re.IGNORECASE), 'dedicación'),
    # gestión (singular only)
    (re.compile(r'\bgestion\b',       re.IGNORECASE), 'gestión'),
    # repetición (singular only)
    (re.compile(r'\brepeticion\b',    re.IGNORECASE), 'repetición'),
    # descripción (singular only)
    (re.compile(r'\bdescripcion\b',   re.IGNORECASE), 'descripción'),
    # perfección (singular only)
    (re.compile(r'\bperfeccion\b',    re.IGNORECASE), 'perfección'),
    # definición (singular only)
    (re.compile(r'\bdefinicion\b',    re.IGNORECASE), 'definición'),
    # condición (singular only)
    (re.compile(r'\bcondicion\b',     re.IGNORECASE), 'condición'),
    # percepción (already above)
    # posición (already above)
    # fácil/es
    (re.compile(r'\bfacil\b',         re.IGNORECASE), 'fácil'),
    (re.compile(r'\bfaciles\b',       re.IGNORECASE), 'fáciles'),
    # difícil/es
    (re.compile(r'\bdificil\b',       re.IGNORECASE), 'difícil'),
    (re.compile(r'\bdificiles\b',     re.IGNORECASE), 'difíciles'),
    # único/a/os/as (never a verb form)
    (re.compile(r'\bunico\b',         re.IGNORECASE), 'único'),
    (re.compile(r'\bunica\b',         re.IGNORECASE), 'única'),
    (re.compile(r'\bunicos\b',        re.IGNORECASE), 'únicos'),
    (re.compile(r'\bunicas\b',        re.IGNORECASE), 'únicas'),
    # móvil/es (noun/adjective only; no verb "movilarse")
    (re.compile(r'\bmovil\b',         re.IGNORECASE), 'móvil'),
    (re.compile(r'\bmoviles\b',       re.IGNORECASE), 'móviles'),
    # éxito/s (noun only)
    (re.compile(r'\bexito\b',         re.IGNORECASE), 'éxito'),
    (re.compile(r'\bexitos\b',        re.IGNORECASE), 'éxitos'),
    # débil/es (adjective only)
    (re.compile(r'\bdebil\b',         re.IGNORECASE), 'débil'),
    (re.compile(r'\bdebiles\b',       re.IGNORECASE), 'débiles'),
    # ágil/es (adjective only)
    (re.compile(r'\bagil\b',          re.IGNORECASE), 'ágil'),
    (re.compile(r'\bagiles\b',        re.IGNORECASE), 'ágiles'),
    # cómodo/a/os/as (adjective only)
    (re.compile(r'\bcomodo\b',        re.IGNORECASE), 'cómodo'),
    (re.compile(r'\bcomoda\b',        re.IGNORECASE), 'cómoda'),
    (re.compile(r'\bcomodos\b',       re.IGNORECASE), 'cómodos'),
    (re.compile(r'\bcomodas\b',       re.IGNORECASE), 'cómodas'),
    # óptimo/a/os/as (adjective only)
    (re.compile(r'\boptimo\b',        re.IGNORECASE), 'óptimo'),
    (re.compile(r'\boptima\b',        re.IGNORECASE), 'óptima'),
    (re.compile(r'\boptimos\b',       re.IGNORECASE), 'óptimos'),
    (re.compile(r'\boptimas\b',       re.IGNORECASE), 'óptimas'),
    # rápido/a/os/as, rápidamente (adjective only)
    (re.compile(r'\brapido\b',        re.IGNORECASE), 'rápido'),
    (re.compile(r'\brapida\b',        re.IGNORECASE), 'rápida'),
    (re.compile(r'\brapidos\b',       re.IGNORECASE), 'rápidos'),
    (re.compile(r'\brapidas\b',       re.IGNORECASE), 'rápidas'),
    (re.compile(r'\brapidamente\b',   re.IGNORECASE), 'rápidamente'),
    # mínimo/a/os/as (adjective/noun only)
    (re.compile(r'\bminimo\b',        re.IGNORECASE), 'mínimo'),
    (re.compile(r'\bminima\b',        re.IGNORECASE), 'mínima'),
    (re.compile(r'\bminimos\b',       re.IGNORECASE), 'mínimos'),
    (re.compile(r'\bminimas\b',       re.IGNORECASE), 'mínimas'),
    # máximo/a/os/as (adjective/noun only)
    (re.compile(r'\bmaximo\b',        re.IGNORECASE), 'máximo'),
    (re.compile(r'\bmaximo\b',        re.IGNORECASE), 'máximo'),  # already above
    # simultáneo/a/os/as (adjective only)
    (re.compile(r'\bsimultaneo\b',    re.IGNORECASE), 'simultáneo'),
    (re.compile(r'\bsimultanea\b',    re.IGNORECASE), 'simultánea'),
    (re.compile(r'\bsimultaneos\b',   re.IGNORECASE), 'simultáneos'),
    (re.compile(r'\bsimultaneas\b',   re.IGNORECASE), 'simultáneas'),
    # cíclico/a/os/as (adjective only)
    (re.compile(r'\bciclico\b',       re.IGNORECASE), 'cíclico'),
    (re.compile(r'\bciclica\b',       re.IGNORECASE), 'cíclica'),
    (re.compile(r'\bciclicos\b',      re.IGNORECASE), 'cíclicos'),
    (re.compile(r'\bciclicas\b',      re.IGNORECASE), 'cíclicas'),
    # útil/es (adjective only)
    (re.compile(r'\butil\b',          re.IGNORECASE), 'útil'),
    (re.compile(r'\butiles\b',        re.IGNORECASE), 'útiles'),
    # símbolo/s (noun only)
    (re.compile(r'\bsimbolo\b',       re.IGNORECASE), 'símbolo'),
    (re.compile(r'\bsimbolos\b',      re.IGNORECASE), 'símbolos'),
    # espíritu (noun only)
    (re.compile(r'\bespiritu\b',      re.IGNORECASE), 'espíritu'),
    # líquido/s (noun/adjective only)
    (re.compile(r'\bliquido\b',       re.IGNORECASE), 'líquido'),
    (re.compile(r'\bliquidos\b',      re.IGNORECASE), 'líquidos'),
    # ánimo (0 usos como verbo en los libros — SEGURO)
    (re.compile(r'\banimo\b',         re.IGNORECASE), 'ánimo'),
    (re.compile(r'\banimos\b',        re.IGNORECASE), 'ánimos'),
    # límite/s (0 usos como verbo subjuntivo en los libros — SEGURO)
    (re.compile(r'\blimite\b',        re.IGNORECASE), 'límite'),
    (re.compile(r'\blimites\b',       re.IGNORECASE), 'límites'),
    # EXCLUIDOS por ambigüedad verbo/sustantivo verificada:
    # válido/a (4 usos de "haya valido" como participio de valer)
    # título/s (0 instancias sin tilde en los libros)
    # público/a (publicar verbo)
]

def fix_esdrujulas(line):
    for pattern, repl in ESDRUJ_FIXES:
        def _repl(m, r=repl):
            orig = m.group(0)
            if orig[0].isupper():
                return r[0].upper() + r[1:]
            return r
        line = pattern.sub(_repl, line)
    return line


# 8. Adverbios y palabras monosílabas/bisílabas sin tilde
ADV_FIXES = [
    (re.compile(r'\bsegun\b',    re.IGNORECASE), 'según'),
    (re.compile(r'\btodavia\b',  re.IGNORECASE), 'todavía'),
    (re.compile(r'\btambien\b',  re.IGNORECASE), 'también'),
    (re.compile(r'\bdespues\b',  re.IGNORECASE), 'después'),
    (re.compile(r'\bademas\b',   re.IGNORECASE), 'además'),
    (re.compile(r'\batras\b',    re.IGNORECASE), 'atrás'),
    (re.compile(r'\baqui\b',     re.IGNORECASE), 'aquí'),
    (re.compile(r'\balli\b',     re.IGNORECASE), 'allí'),
    (re.compile(r'\bahi\b',      re.IGNORECASE), 'ahí'),
    (re.compile(r'\basi\b',      re.IGNORECASE), 'así'),
    (re.compile(r'\bdetras\b',  re.IGNORECASE), 'detrás'),
    (re.compile(r'\bquizas\b',  re.IGNORECASE), 'quizás'),
    (re.compile(r'\bjamas\b',   re.IGNORECASE), 'jamás'),
    # 'aún' (still/yet) vs 'aun' (even) — fix only obvious "still" uses
    # Skip: too ambiguous between 'aun cuando' (even when) vs 'aún no' (still not)
]

def fix_adverbs(line):
    for pattern, repl in ADV_FIXES:
        def _repl(m, r=repl):
            orig = m.group(0)
            if orig[0].isupper():
                return r[0].upper() + r[1:]
            return r
        line = pattern.sub(_repl, line)
    return line


# ── Procesado por línea ──────────────────────────────────────────────────────

def fix_line(line):
    stripped = line.strip()
    if not stripped:
        return line
    # Código, tablas y citas: no tocar
    if stripped.startswith(('`', '|', '>')):
        return line
    # Encabezados: aplicar fixes de palabras (esdrújulas, adverbios, está+gerundio)
    if stripped.startswith('#'):
        line = fix_encoding(line)
        line = fix_esta(line)
        line = fix_esdrujulas(line)
        line = fix_adverbs(line)
        return line

    line = fix_encoding(line)
    line = fix_modelo(line)
    line = fix_conditional(line)
    line = fix_imperfect(line)
    line = fix_imperatives(line)
    line = fix_esta(line)
    line = fix_esdrujulas(line)
    line = fix_adverbs(line)
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
