"""
Add copyright, disclaimer and About the Author to all 14 Mother Books.
Idempotent: skips files that already have the copyright line.
"""

import os, re

BASE = r"c:\Users\usuario\Desktop\IA\Libros"

MOTHER_BOOKS = [
    # (path, language, collection_label, footer_line)
    (
        r"AI_Artificial_Intelligence\00_Mother_Book\The_NOVA_Method.md", "en",
        "AI Applied Intelligence Collection",
        "*Mother Book of the AI Applied Intelligence Collection — 100 books in 10 series.*",
    ),
    (
        r"Applied_Psychology\00_Mother_Book\The_MIND_Method.md", "en",
        "Applied Psychology Collection",
        "*Mother Book of the Applied Psychology Collection — 100 books in 10 series.*",
    ),
    (
        r"Entrepreneurship\00_Mother_Book\The_LAUNCH_Method.md", "en",
        "Entrepreneurship Collection",
        "*Mother Book of the Entrepreneurship Collection — 100 books in 10 series.*",
    ),
    (
        r"Health_Wellness\00_Mother_Book\The_RESET_Method.md", "en",
        "Health and Wellness Collection",
        "*Mother Book of the Health and Wellness Collection — 100 books in 10 series.*",
    ),
    (
        r"Personal_Finance\00_Mother_Book\The_5P_Method.md", "en",
        "Personal Finance Collection",
        "*Mother Book of the Personal Finance Collection — 100 books in 10 series.*",
    ),
    (
        r"Productivity_Success\00_Mother_Book\The_ACTION_Method.md", "en",
        "Productivity and Success Collection",
        "*Mother Book of the Productivity and Success Collection — 100 books in 10 series.*",
    ),
    (
        r"Relationships_Communication\00_Mother_Book\The_BOND_Method.md", "en",
        "Relationships and Communication Collection",
        "*Mother Book of the Relationships and Communication Collection — 100 books in 10 series.*",
    ),
    (
        r"IA_Inteligencia_Artificial\00_Libro_Madre\El_Metodo_NOVA.md", "es",
        "Inteligencia Artificial Aplicada",
        "*Libro Madre de la colección Inteligencia Artificial Aplicada — 100 libros en 10 series.*",
    ),
    (
        r"Psicologia_Aplicada\00_Libro_Madre\El_Metodo_MENTE.md", "es",
        "Colección Psicología Aplicada",
        "*Libro Madre de la Colección Psicología Aplicada — 100 libros en 10 series.*",
    ),
    (
        r"Emprendimiento\00_Libro_Madre\El_Metodo_LANZAR.md", "es",
        "Colección Emprendimiento",
        "*Libro Madre de la Colección Emprendimiento — 100 libros en 10 series.*",
    ),
    (
        r"Salud_Bienestar\00_Libro_Madre\El_Metodo_RESET.md", "es",
        "Colección Salud y Bienestar",
        "*Libro Madre de la Colección Salud y Bienestar — 100 libros en 10 series.*",
    ),
    (
        r"Finanzas_Personales\00_Libro_Madre\El_Metodo_5P.md", "es",
        "Colección Finanzas Personales",
        "*Libro Madre de la Colección Finanzas Personales — 100 libros en 10 series.*",
    ),
    (
        r"Productividad_Exito\00_Libro_Madre\El_Metodo_ACCION.md", "es",
        "Colección Productividad y Éxito",
        "*Libro Madre de la Colección Productividad y Éxito — 100 libros en 10 series.*",
    ),
    (
        r"Relaciones_Comunicacion\00_Libro_Madre\El_Metodo_VINCULO.md", "es",
        "Colección Relaciones y Comunicación",
        "*Libro Madre de la Colección Relaciones y Comunicación — 100 libros en 10 series.*",
    ),
]

# ── Front matter blocks ──────────────────────────────────────────────────────

FRONT_EN = """---

*Copyright © 2026 Enrique Padrón. All rights reserved. No part of this publication may be reproduced, distributed, or transmitted in any form or by any means without the prior written permission of the author.*

---

> **Disclaimer:** This book is intended for informational and educational purposes only. The content reflects research, evidence-based frameworks, and practical tools, but is not a substitute for professional medical, psychological, psychiatric, or financial advice. The author and publisher make no representations or warranties regarding the accuracy, applicability, or completeness of the contents. If you are experiencing mental health difficulties, medical conditions, or financial distress, please consult a qualified professional. Individual results will vary. The use of information in this book is at the reader's own risk.

---
"""

FRONT_ES = """---

*Copyright © 2026 Enrique Padrón. Todos los derechos reservados. Ninguna parte de esta publicación puede ser reproducida, distribuida ni transmitida de ninguna forma ni por ningún medio sin el permiso previo por escrito del autor.*

---

> **Aviso legal:** Este libro tiene una finalidad exclusivamente informativa y educativa. El contenido recoge investigación, marcos basados en evidencia y herramientas prácticas, pero no sustituye el consejo médico, psicológico, psiquiátrico ni financiero profesional. El autor y el editor no garantizan la exactitud, aplicabilidad ni exhaustividad del contenido. Si atraviesas dificultades de salud mental, condiciones médicas o problemas financieros, consulta a un profesional cualificado. Los resultados individuales pueden variar. El uso de la información de este libro es responsabilidad exclusiva del lector.

---
"""

# ── Back matter blocks ───────────────────────────────────────────────────────

def back_matter_en(footer):
    return f"""
---

{footer}

---

*If you found this book valuable, please consider leaving a review on Amazon. It takes less than a minute and makes a real difference for independent authors.*

---

## About the Author

Enrique Padrón was born in the Canary Islands, Spain. Twenty-five years across different companies taught him something few dare to say out loud: people don't fail because they lack information. They fail because nobody gave them the right tools at the right moment. This collection exists to change that. Each book distills what truly works — no filler, no empty theory. Developed with the support of artificial intelligence to carry that knowledge further than any single author could reach alone.
"""

def back_matter_es(footer):
    return f"""
---

{footer}

---

*Si este libro te ha resultado útil, considera dejar una reseña en Amazon. Solo lleva un minuto y marca una gran diferencia para los autores independientes.*

---

## Sobre el Autor

Enrique Padrón nació en las Islas Canarias, España. Veinticinco años en distintas empresas le enseñaron algo que pocos se atreven a decir: las personas no fracasan por falta de información. Fracasan porque nadie les dio las herramientas correctas en el momento exacto. Esta colección existe para cambiar eso. Cada libro destila lo que realmente funciona, sin relleno, sin teoría vacía. Desarrollada con el apoyo de inteligencia artificial para llevar ese conocimiento más lejos de lo que cualquier autor podría alcanzar solo.
"""


# ── Main ─────────────────────────────────────────────────────────────────────

def patch(rel_path, lang, _col, footer):
    path = os.path.join(BASE, rel_path)
    with open(path, encoding="utf-8-sig") as f:
        content = f.read()

    # Idempotency check
    if "Copyright © 2026" in content:
        print(f"  SKIP (ya tiene copyright): {os.path.basename(path)}")
        return

    # Strip any existing old footer/about section to avoid duplicates
    # Remove trailing "Mother Book of..." line if present
    content = re.sub(
        r'\n---\n\n\*Mother Book of.*?\*\s*$', '', content, flags=re.DOTALL
    )
    content = re.sub(
        r'\n---\n\n\*Libro Madre de.*?\*\s*$', '', content, flags=re.DOTALL
    )
    content = content.rstrip()

    # Find insertion point: after the first "---" separator (after collection line)
    # Pattern: title \n\n subtitle \n\n collection_line \n\n ---
    first_sep = content.find("\n---\n")
    if first_sep == -1:
        # No separator yet — insert after the 4th line (title, sub, blank, collection)
        lines = content.split("\n")
        header = "\n".join(lines[:4])
        body   = "\n".join(lines[4:])
        front  = FRONT_EN if lang == "en" else FRONT_ES
        new_content = header + "\n" + front + body
    else:
        # Insert front matter right after the first ---
        before = content[:first_sep]
        after  = content[first_sep + 5:]  # skip "\n---\n"
        front  = FRONT_EN if lang == "en" else FRONT_ES
        new_content = before + "\n" + front + after

    # Append back matter
    back = back_matter_en(footer) if lang == "en" else back_matter_es(footer)
    new_content = new_content.rstrip() + "\n" + back

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"  OK: {os.path.basename(path)}")


print("Añadiendo copyright, disclaimer y About the Author a los 14 Libros Madre...\n")
for args in MOTHER_BOOKS:
    patch(*args)
print("\nListo.")
