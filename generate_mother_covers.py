"""
Generate covers for all 14 Mother Books (000.jpg).
Design: dark premium background, gold accent, "Complete Guide" badge.
Output: 1600x2560 JPG in each collection's images folder.
"""

import os, asyncio
from playwright.async_api import async_playwright

BASE = r"c:\Users\usuario\Desktop\IA\Libros"

MOTHER_BOOKS = [
    # EN collections
    {
        "out":      r"AI_Artificial_Intelligence\Covers\images\000.jpg",
        "title":    "THE NOVA\nMETHOD",
        "subtitle": "Your Complete Guide to Understanding,\nUsing, and Thriving in the Age of AI",
        "col":      "AI & Applied Intelligence",
        "lang":     "en",
        "c1": "#0d1b2a", "c2": "#1b3a5c", "accent": "#4fc3f7",
    },
    {
        "out":      r"Applied_Psychology\Covers\images\000.jpg",
        "title":    "THE MIND\nMETHOD",
        "subtitle": "Applied Psychology to Understand\nand Transform Yourself",
        "col":      "Applied Psychology Collection",
        "lang":     "en",
        "c1": "#1a0a2e", "c2": "#3d1f6e", "accent": "#ce93d8",
    },
    {
        "out":      r"Entrepreneurship\Covers\images\000.jpg",
        "title":    "THE LAUNCH\nMETHOD",
        "subtitle": "What Business Schools Don't Teach You\nAbout Entrepreneurship",
        "col":      "Entrepreneurship Collection",
        "lang":     "en",
        "c1": "#1a0d00", "c2": "#4a2000", "accent": "#ffb74d",
    },
    {
        "out":      r"Health_Wellness\Covers\images\000.jpg",
        "title":    "THE RESET\nMETHOD",
        "subtitle": "The Health System\nNobody Taught You",
        "col":      "Health & Wellness Collection",
        "lang":     "en",
        "c1": "#001a0d", "c2": "#003d1f", "accent": "#66bb6a",
    },
    {
        "out":      r"Personal_Finance\Covers\images\000.jpg",
        "title":    "THE 5P\nMETHOD",
        "subtitle": "What Nobody Taught You\nAbout Money",
        "col":      "Personal Finance Collection",
        "lang":     "en",
        "c1": "#001a1a", "c2": "#00404a", "accent": "#ffd54f",
    },
    {
        "out":      r"Productivity_Success\Covers\images\000.jpg",
        "title":    "THE ACTION\nMETHOD",
        "subtitle": "The Productivity System That\nCuts Through the Noise",
        "col":      "Productivity & Success Collection",
        "lang":     "en",
        "c1": "#1a0500", "c2": "#4a1000", "accent": "#ff8a65",
    },
    {
        "out":      r"Relationships_Communication\Covers\images\000.jpg",
        "title":    "THE BOND\nMETHOD",
        "subtitle": "What Nobody Taught You About\nConnecting for Real",
        "col":      "Relationships & Communication",
        "lang":     "en",
        "c1": "#1a0010", "c2": "#4a0030", "accent": "#f48fb1",
    },
    # ES collections
    {
        "out":      r"IA_Inteligencia_Artificial\Portadas\images\000.jpg",
        "title":    "EL MÉTODO\nNOVA",
        "subtitle": "Guía para entender, usar y prosperar\nen la era de la inteligencia artificial",
        "col":      "Inteligencia Artificial Aplicada",
        "lang":     "es",
        "c1": "#0d1b2a", "c2": "#1b3a5c", "accent": "#4fc3f7",
    },
    {
        "out":      r"Psicologia_Aplicada\Portadas\images\000.jpg",
        "title":    "EL MÉTODO\nMENTE",
        "subtitle": "Psicología práctica para\nentenderte y transformarte",
        "col":      "Colección Psicología Aplicada",
        "lang":     "es",
        "c1": "#1a0a2e", "c2": "#3d1f6e", "accent": "#ce93d8",
    },
    {
        "out":      r"Emprendimiento\Portadas\images\000.jpg",
        "title":    "EL MÉTODO\nLANZAR",
        "subtitle": "Lo que las escuelas de negocio no\nte enseñan sobre emprender",
        "col":      "Colección Emprendimiento",
        "lang":     "es",
        "c1": "#1a0d00", "c2": "#4a2000", "accent": "#ffb74d",
    },
    {
        "out":      r"Salud_Bienestar\Portadas\images\000.jpg",
        "title":    "EL MÉTODO\nRESET",
        "subtitle": "El sistema que nadie te enseñó\npara tener salud real",
        "col":      "Colección Salud y Bienestar",
        "lang":     "es",
        "c1": "#001a0d", "c2": "#003d1f", "accent": "#66bb6a",
    },
    {
        "out":      r"Finanzas_Personales\Portadas\images\000.jpg",
        "title":    "EL MÉTODO\n5P",
        "subtitle": "Lo que nadie te enseñó\nsobre el dinero",
        "col":      "Colección Finanzas Personales",
        "lang":     "es",
        "c1": "#001a1a", "c2": "#00404a", "accent": "#ffd54f",
    },
    {
        "out":      r"Productividad_Exito\Portadas\images\000.jpg",
        "title":    "EL MÉTODO\nACCIÓN",
        "subtitle": "El sistema que nadie te enseñó para\nrendir más sin trabajar más",
        "col":      "Colección Productividad y Éxito",
        "lang":     "es",
        "c1": "#1a0500", "c2": "#4a1000", "accent": "#ff8a65",
    },
    {
        "out":      r"Relaciones_Comunicacion\Portadas\images\000.jpg",
        "title":    "EL MÉTODO\nVÍNCULO",
        "subtitle": "Lo que nadie te enseñó sobre\ncómo conectar de verdad",
        "col":      "Colección Relaciones y Comunicación",
        "lang":     "es",
        "c1": "#1a0010", "c2": "#4a0030", "accent": "#f48fb1",
    },
]

BADGE_EN = "COMPLETE COLLECTION GUIDE"
BADGE_ES = "GUÍA COMPLETA DE LA COLECCIÓN"
AUTHOR   = "Enrique Padrón"


def make_html(book):
    badge = BADGE_ES if book["lang"] == "es" else BADGE_EN
    title_lines = book["title"].split("\n")
    sub_lines   = book["subtitle"].split("\n")
    c1, c2, ac  = book["c1"], book["c2"], book["accent"]

    # Title HTML — second line is the keyword (NOVA, MIND, etc.) in accent color
    t1 = title_lines[0] if len(title_lines) > 0 else ""
    t2 = title_lines[1] if len(title_lines) > 1 else ""
    subtitle_html = "<br>".join(sub_lines)

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: 1600px; height: 2560px; overflow: hidden;
    background: linear-gradient(160deg, {c1} 0%, {c2} 55%, #000 100%);
    font-family: 'Georgia', serif;
    color: #fff;
    position: relative;
  }}

  /* diagonal accent stripe */
  .stripe {{
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(
      135deg,
      transparent 0%,
      transparent 38%,
      {ac}18 38.5%,
      {ac}08 42%,
      transparent 42.5%
    );
  }}

  /* top accent bar */
  .top-bar {{
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 8px;
    background: {ac};
  }}

  /* badge */
  .badge {{
    position: absolute;
    top: 80px;
    left: 100px; right: 100px;
    text-align: center;
    font-size: 32px;
    letter-spacing: 6px;
    color: {ac};
    text-transform: uppercase;
    font-family: 'Arial Narrow', 'Arial', sans-serif;
    font-weight: 400;
    border-top: 1px solid {ac}55;
    border-bottom: 1px solid {ac}55;
    padding: 16px 0;
  }}

  /* large decorative symbol */
  .deco {{
    position: absolute;
    top: 220px; right: 90px;
    font-size: 320px;
    color: {ac}15;
    font-family: 'Arial', sans-serif;
    line-height: 1;
    font-weight: 900;
    letter-spacing: -20px;
  }}

  /* title area */
  .title-wrap {{
    position: absolute;
    top: 320px;
    left: 100px; right: 100px;
  }}
  .title-line1 {{
    font-size: 96px;
    color: #ffffffcc;
    letter-spacing: 14px;
    text-transform: uppercase;
    font-family: 'Arial Narrow', 'Arial', sans-serif;
    font-weight: 300;
    line-height: 1.1;
  }}
  .title-line2 {{
    font-size: 148px;
    color: {ac};
    letter-spacing: 6px;
    text-transform: uppercase;
    font-family: 'Arial Black', 'Arial', sans-serif;
    font-weight: 900;
    line-height: 1.0;
    margin-top: -8px;
  }}

  /* divider */
  .divider {{
    position: absolute;
    top: 730px;
    left: 100px;
    width: 180px;
    height: 4px;
    background: {ac};
  }}

  /* subtitle */
  .subtitle {{
    position: absolute;
    top: 790px;
    left: 100px; right: 100px;
    font-size: 54px;
    color: #ffffffaa;
    line-height: 1.45;
    font-style: italic;
    font-family: 'Georgia', serif;
  }}

  /* 10 SERIES dots */
  .series-row {{
    position: absolute;
    top: 1600px;
    left: 100px; right: 100px;
    display: flex;
    gap: 20px;
    align-items: center;
  }}
  .dot {{
    width: 28px; height: 28px;
    border-radius: 50%;
    background: {ac};
    opacity: 0.7;
    flex-shrink: 0;
  }}
  .series-label {{
    font-size: 32px;
    color: {ac}cc;
    letter-spacing: 4px;
    font-family: 'Arial Narrow', 'Arial', sans-serif;
    text-transform: uppercase;
  }}

  /* collection name */
  .collection {{
    position: absolute;
    bottom: 260px;
    left: 100px; right: 100px;
    font-size: 38px;
    color: {ac}99;
    letter-spacing: 5px;
    text-transform: uppercase;
    font-family: 'Arial Narrow', 'Arial', sans-serif;
    text-align: center;
    border-top: 1px solid {ac}33;
    padding-top: 30px;
  }}

  /* author */
  .author {{
    position: absolute;
    bottom: 140px;
    left: 100px; right: 100px;
    font-size: 52px;
    color: #ffffffcc;
    text-align: center;
    letter-spacing: 4px;
    font-family: 'Georgia', serif;
  }}

  /* bottom bar */
  .bottom-bar {{
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 8px;
    background: {ac};
  }}
</style>
</head>
<body>
  <div class="stripe"></div>
  <div class="top-bar"></div>

  <div class="badge">{badge}</div>

  <div class="deco">∞</div>

  <div class="title-wrap">
    <div class="title-line1">{t1}</div>
    <div class="title-line2">{t2}</div>
  </div>

  <div class="divider"></div>
  <div class="subtitle">{subtitle_html}</div>

  <div class="series-row">
    {''.join('<div class="dot"></div>' * 10)}
    <div class="series-label">10 Series · 100 Books</div>
  </div>

  <div class="collection">{book["col"]}</div>
  <div class="author">{AUTHOR}</div>
  <div class="bottom-bar"></div>
</body>
</html>"""


async def generate_all():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page    = await browser.new_page(viewport={"width": 1600, "height": 2560})

        for i, book in enumerate(MOTHER_BOOKS, 1):
            out_path = os.path.join(BASE, book["out"])
            os.makedirs(os.path.dirname(out_path), exist_ok=True)

            html = make_html(book)
            await page.set_content(html)
            await page.wait_for_timeout(300)
            await page.screenshot(path=out_path, type="jpeg", quality=95,
                                  clip={"x":0,"y":0,"width":1600,"height":2560})
            print(f"  [{i}/14] {os.path.basename(book['out'])} — {book['title'].replace(chr(10),' ')}")

        await browser.close()
    print(f"\n14 portadas generadas.")

if __name__ == "__main__":
    asyncio.run(generate_all())
