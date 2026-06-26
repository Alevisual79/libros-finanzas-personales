"""
Amazon Ads Keyword Generator
Genera amazon_ads_plan.csv con campañas, grupos de anuncios y keywords
listos para importar en Amazon Ads cuando los libros estén publicados.

Estructura por colección:
  Campaña 1 — Auto (Amazon elige targets automáticamente)
  Campaña 2 — Manual Broad  (keywords amplias, descubrimiento)
  Campaña 3 — Manual Exact  (keywords exactas, conversión)
  Campaña 4 — Manual ASIN   (competidores, relleno posterior con ASINs reales)
"""

import os, re, csv, sys
sys.path.insert(0, r"C:\Users\usuario\Desktop\IA\Libros")
from generate_metadata_csv import parse_books_meta, _extract_array
from generate_all_covers import _get_str

BASE = r"c:\Users\usuario\Desktop\IA\Libros"

# ── Colecciones con seed keywords especializadas ─────────────────────────────

COLLECTIONS = [
    {
        "name":     "AI & Artificial Intelligence",
        "lang":     "en",
        "html":     "AI_Artificial_Intelligence/Covers/covers.html",
        "daily_budget": 8.00,
        "seeds": [
            "artificial intelligence books", "machine learning book", "AI explained",
            "understanding artificial intelligence", "AI for beginners", "deep learning book",
            "ChatGPT book", "future of AI", "artificial intelligence guide",
            "technology books nonfiction", "AI and society", "neural networks explained",
        ],
        "competitors": [  # Autores/libros top del nicho — rellenar ASINs reales
            "Life 3.0 Max Tegmark", "Human Compatible Stuart Russell",
            "The AI Advantage Thomas Davenport",
        ],
    },
    {
        "name":     "Applied Psychology",
        "lang":     "en",
        "html":     "Applied_Psychology/Covers/covers.html",
        "daily_budget": 10.00,
        "seeds": [
            "psychology books bestseller", "applied psychology", "cognitive behavioral therapy book",
            "understanding emotions book", "mental health self help", "psychology of behavior",
            "anxiety self help book", "self esteem book", "trauma healing book",
            "psychology for everyday life", "behavioral science book", "emotional intelligence book",
        ],
        "competitors": [
            "Thinking Fast and Slow Kahneman", "The Body Keeps the Score van der Kolk",
            "Man Search for Meaning Frankl",
        ],
    },
    {
        "name":     "Entrepreneurship",
        "lang":     "en",
        "html":     "Entrepreneurship/Covers/covers.html",
        "daily_budget": 8.00,
        "seeds": [
            "entrepreneurship book", "startup guide", "how to start a business",
            "small business book", "business mindset", "entrepreneur mindset book",
            "building a business", "business strategy book", "side hustle book",
            "solopreneur book", "online business book", "business growth book",
        ],
        "competitors": [
            "Zero to One Peter Thiel", "The Lean Startup Ries", "$100 Startup Chris Guillebeau",
        ],
    },
    {
        "name":     "Health and Wellness",
        "lang":     "en",
        "html":     "Health_Wellness/Covers/covers.html",
        "daily_budget": 10.00,
        "seeds": [
            "health and wellness book", "healthy lifestyle book", "nutrition book",
            "better sleep book", "fitness guide book", "weight loss mindset",
            "gut health book", "stress management book", "wellness habits book",
            "healthy habits book", "mind body connection book", "holistic health book",
        ],
        "competitors": [
            "How Not to Die Greger", "Atomic Habits James Clear",
            "Why We Sleep Matthew Walker",
        ],
    },
    {
        "name":     "Personal Finance",
        "lang":     "en",
        "html":     "Personal_Finance/Covers/covers.html",
        "daily_budget": 12.00,
        "seeds": [
            "personal finance book", "money management book", "how to save money",
            "investing for beginners", "financial freedom book", "get out of debt book",
            "budgeting book", "wealth building book", "financial literacy book",
            "passive income book", "retire early book", "money mindset book",
        ],
        "competitors": [
            "Rich Dad Poor Dad Kiyosaki", "The Total Money Makeover Ramsey",
            "I Will Teach You to Be Rich Sethi",
        ],
    },
    {
        "name":     "Productivity & Success",
        "lang":     "en",
        "html":     "Productivity_Success/Covers/covers.html",
        "daily_budget": 10.00,
        "seeds": [
            "productivity book", "time management book", "success habits book",
            "goal setting book", "focus book", "getting things done book",
            "deep work book", "morning routine book", "high performance habits",
            "procrastination book", "discipline book", "self improvement book",
        ],
        "competitors": [
            "Atomic Habits James Clear", "Deep Work Cal Newport",
            "The One Thing Gary Keller",
        ],
    },
    {
        "name":     "Relationships & Communication",
        "lang":     "en",
        "html":     "Relationships_Communication/Covers/covers.html",
        "daily_budget": 10.00,
        "seeds": [
            "relationships book", "communication skills book", "how to communicate better",
            "healthy relationships book", "boundaries book", "toxic relationships book",
            "couples book", "family relationships book", "social skills book",
            "conflict resolution book", "emotional intelligence relationships", "dating book",
        ],
        "competitors": [
            "The Five Love Languages Chapman", "Attached Levine Heller",
            "Set Boundaries Find Peace Nedra Tawwab",
        ],
    },
    # Colecciones ES
    {
        "name":     "IA e Inteligencia Artificial",
        "lang":     "es",
        "html":     "IA_Inteligencia_Artificial/Portadas/portadas.html",
        "daily_budget": 5.00,
        "seeds": [
            "inteligencia artificial libro", "machine learning libro",
            "IA explicada", "inteligencia artificial para principiantes",
            "futuro inteligencia artificial", "libro tecnologia",
            "automatizacion trabajo", "ChatGPT libro español",
        ],
        "competitors": ["La cuarta revolucion industrial Schwab"],
    },
    {
        "name":     "Psicologia Aplicada",
        "lang":     "es",
        "html":     "Psicologia_Aplicada/Portadas/portadas.html",
        "daily_budget": 8.00,
        "seeds": [
            "psicologia libro", "psicologia aplicada", "salud mental libro",
            "autoayuda psicologia", "inteligencia emocional libro",
            "ansiedad libro", "autoestima libro", "trauma libro español",
            "psicologia practica", "bienestar mental libro",
        ],
        "competitors": ["El poder del ahora Tolle", "Los cuatro acuerdos Ruiz"],
    },
    {
        "name":     "Emprendimiento",
        "lang":     "es",
        "html":     "Emprendimiento/Portadas/portadas.html",
        "daily_budget": 6.00,
        "seeds": [
            "emprendimiento libro", "como emprender", "startup libro español",
            "negocio propio libro", "emprendedor libro", "crear empresa libro",
            "mentalidad emprendedora", "negocios online libro",
        ],
        "competitors": ["El emprendedor del minuto Blanchard"],
    },
    {
        "name":     "Salud y Bienestar",
        "lang":     "es",
        "html":     "Salud_Bienestar/Portadas/portadas.html",
        "daily_budget": 8.00,
        "seeds": [
            "salud y bienestar libro", "habitos saludables libro",
            "nutricion libro español", "dormir mejor libro",
            "estilo de vida saludable", "libro bienestar", "adelgazar sin dieta libro",
            "ejercicio habitos libro", "reset salud libro",
        ],
        "competitors": ["El metodo Gabriel Jon Gabriel", "Come bien hoy"],
    },
    {
        "name":     "Finanzas Personales",
        "lang":     "es",
        "html":     "Finanzas_Personales/Portadas/portadas.html",
        "daily_budget": 10.00,
        "seeds": [
            "finanzas personales libro", "como ahorrar dinero libro",
            "invertir para principiantes libro", "libertad financiera libro",
            "deudas libro español", "dinero libro autoayuda",
            "presupuesto personal libro", "independencia financiera",
            "habitos financieros libro", "mentalidad millonaria libro",
        ],
        "competitors": ["Padre rico padre pobre Kiyosaki español",
                        "El hombre mas rico de babilonia Clason"],
    },
    {
        "name":     "Productividad y Exito",
        "lang":     "es",
        "html":     "Productividad_Exito/Portadas/portadas.html",
        "daily_budget": 7.00,
        "seeds": [
            "productividad libro español", "gestion del tiempo libro",
            "habitos exito libro", "objetivos libro español",
            "disciplina libro", "procrastinacion libro",
            "superacion personal libro", "exito profesional libro",
        ],
        "competitors": ["Habitos atomicos español Clear", "Los 7 habitos Covey"],
    },
    {
        "name":     "Relaciones y Comunicacion",
        "lang":     "es",
        "html":     "Relaciones_Comunicacion/Portadas/portadas.html",
        "daily_budget": 7.00,
        "seeds": [
            "relaciones personales libro", "comunicacion libro español",
            "limites relaciones libro", "relaciones toxicas libro",
            "amor y apego libro", "habilidades sociales libro",
            "pareja libro autoayuda", "familia relaciones libro",
        ],
        "competitors": ["Los cinco lenguajes del amor Chapman",
                        "Vinculados Levine Heller español"],
    },
]

# ── Keyword extraction from book titles ─────────────────────────────────────

STOPWORDS_EN = {"the","a","an","and","or","of","in","on","at","to","for",
                "with","your","how","what","why","when","who","this","that",
                "is","are","was","were","be","been","have","has","its","as"}
STOPWORDS_ES = {"el","la","los","las","un","una","unos","unas","y","o","de",
                "en","con","para","por","que","se","su","sus","al","del",
                "lo","le","les","me","te","nos"}

def title_keywords(books, lang):
    """Extract 2-3 word phrases from book titles as long-tail keywords."""
    stopwords = STOPWORDS_EN if lang == "en" else STOPWORDS_ES
    seen = set()
    kws = []
    for b in books:
        title = b.get("title","").lower()
        words = [w for w in re.findall(r'\b[a-záéíóúüñ]{3,}\b', title) if w not in stopwords]
        # 2-word combos
        for i in range(len(words)-1):
            kw = f"{words[i]} {words[i+1]}"
            if kw not in seen:
                seen.add(kw)
                kws.append(kw)
        # single meaningful words > 5 chars
        for w in words:
            if len(w) > 5 and w not in seen:
                seen.add(w)
                kws.append(w)
    return kws[:60]  # top 60


# ── Campaign structure builder ───────────────────────────────────────────────

def build_campaigns(col, books):
    rows = []
    name    = col["name"]
    lang    = col["lang"]
    budget  = col["daily_budget"]
    seeds   = col["seeds"]
    title_kws = title_keywords(books, lang)

    # Bid recommendations (Amazon books niche, 2025)
    BID_AUTO   = 0.35
    BID_BROAD  = 0.30
    BID_EXACT  = 0.45
    BID_ASIN   = 0.40

    # ── Campaign 1: Auto ────────────────────────────────────────────────────
    rows.append({
        "collection":    name,
        "campaign":      f"{name} | Auto",
        "campaign_type": "Sponsored Products",
        "targeting":     "Auto",
        "ad_group":      "auto_all",
        "keyword":       "(auto — Amazon elige targets)",
        "match_type":    "Auto",
        "bid_usd":       BID_AUTO,
        "daily_budget":  budget * 0.30,
        "language":      lang,
        "notes":         "Lanzar primero. Dejar 2 semanas. Minar search terms para Manual.",
    })

    # ── Campaign 2: Manual Broad ────────────────────────────────────────────
    for kw in seeds:
        rows.append({
            "collection":    name,
            "campaign":      f"{name} | Manual Broad",
            "campaign_type": "Sponsored Products",
            "targeting":     "Keyword",
            "ad_group":      "broad_seeds",
            "keyword":       kw,
            "match_type":    "Broad",
            "bid_usd":       BID_BROAD,
            "daily_budget":  budget * 0.35,
            "language":      lang,
            "notes":         "Descubrimiento. Revisar semanalmente, pausar keywords con alto ACOS.",
        })

    # ── Campaign 3: Manual Exact (long-tail from titles) ───────────────────
    for kw in title_kws[:30]:
        rows.append({
            "collection":    name,
            "campaign":      f"{name} | Manual Exact",
            "campaign_type": "Sponsored Products",
            "targeting":     "Keyword",
            "ad_group":      "exact_titles",
            "keyword":       kw + (" book" if lang == "en" else " libro"),
            "match_type":    "Exact",
            "bid_usd":       BID_EXACT,
            "daily_budget":  budget * 0.25,
            "language":      lang,
            "notes":         "Long-tail de titulos propios. Alta intención de compra.",
        })

    # ── Campaign 4: ASIN Targeting (competidores) ──────────────────────────
    for comp in col.get("competitors", []):
        rows.append({
            "collection":    name,
            "campaign":      f"{name} | ASIN Competidores",
            "campaign_type": "Sponsored Products",
            "targeting":     "Product (ASIN)",
            "ad_group":      "competitor_asins",
            "keyword":       f"[BUSCAR EN AMAZON: {comp}]",
            "match_type":    "ASIN",
            "bid_usd":       BID_ASIN,
            "daily_budget":  budget * 0.10,
            "language":      lang,
            "notes":         "Reemplazar [BUSCAR EN AMAZON: ...] con el ASIN real (B0XXXXX). Aparecer en paginas de competidores.",
        })

    return rows


# ── Main ─────────────────────────────────────────────────────────────────────

FIELDNAMES = [
    "collection", "campaign", "campaign_type", "targeting",
    "ad_group", "keyword", "match_type", "bid_usd",
    "daily_budget", "language", "notes",
]

out_path = os.path.join(BASE, "amazon_ads_plan.csv")
total_kws = 0
total_budget = 0.0

with open(out_path, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
    writer.writeheader()

    for col in COLLECTIONS:
        html_path = os.path.join(BASE, col["html"])
        try:
            books = parse_books_meta(html_path)
        except Exception as e:
            print(f"  ERROR {col['name']}: {e}")
            books = []

        rows = build_campaigns(col, books)
        writer.writerows(rows)
        total_kws += len(rows)
        total_budget += col["daily_budget"]
        print(f"  {col['name']}: {len(rows)} filas")

print(f"\nTotal filas: {total_kws}")
print(f"Presupuesto diario total (todas las colecciones): ${total_budget:.2f}/dia")
print(f"Presupuesto mensual total: ${total_budget*30:.0f}/mes")
print(f"\nACOS objetivo a $2.99 (70% royalty = $2.08 neto):")
print(f"  Break-even ACOS: {2.08/2.99*100:.0f}%  (gastar hasta $2.08 por venta)")
print(f"  ACOS conservador: 35%  (gastar $1.05 → ganar $1.03 neto)")
print(f"  ACOS agresivo:    55%  (gastar $1.64 → ganar $0.44 neto, prioriza ranking)")
print(f"\nArchivo: {out_path}")
