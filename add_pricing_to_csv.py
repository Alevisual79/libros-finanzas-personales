"""Add price columns to kdp_metadata.csv."""
import csv, os

BASE     = r"c:\Users\usuario\Desktop\IA\Libros"
IN_PATH  = os.path.join(BASE, "kdp_metadata.csv")
OUT_PATH = os.path.join(BASE, "kdp_metadata.csv")

PRICE_REGULAR = 2.99   # USD — 70% royalty = $2.08 net
PRICE_MOTHER  = 0.99   # USD — 35% royalty = $0.35 net (loss leader)
ROYALTY_70    = 0.70
ROYALTY_35    = 0.35
DELIVERY_FEE  = 0.009  # ~$0.009 per book @ 150 KB

with open(IN_PATH, encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

fieldnames = list(rows[0].keys())
new_fields = ["price_usd", "price_eur", "royalty_pct", "net_usd", "kdp_select"]
for field in new_fields:
    if field not in fieldnames:
        fieldnames.append(field)

for row in rows:
    num = int(row.get("num", 0))
    is_mother = (num == 0)

    price_usd   = PRICE_MOTHER if is_mother else PRICE_REGULAR
    royalty_pct = ROYALTY_35   if is_mother else ROYALTY_70
    delivery    = 0 if is_mother else DELIVERY_FEE
    net_usd     = round(price_usd * royalty_pct - delivery, 3)

    # EUR: Amazon applies exchange; standard equivalent
    price_eur = 0.99 if is_mother else 2.99

    row["price_usd"]    = f"{price_usd:.2f}"
    row["price_eur"]    = f"{price_eur:.2f}"
    row["royalty_pct"]  = f"{int(royalty_pct*100)}%"
    row["net_usd"]      = f"{net_usd:.3f}"
    row["kdp_select"]   = "No"

with open(OUT_PATH, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# Summary
regular = [r for r in rows if int(r["num"]) > 0]
mothers  = [r for r in rows if int(r["num"]) == 0]
print(f"Libros regulares: {len(regular)} x $2.99 = ${len(regular)*2.08:,.0f} net si 1 venta c/u")
print(f"Libros Madre:     {len(mothers)} x $0.99 = ${len(mothers)*0.35:.0f} net si 1 venta c/u")
print(f"Total filas actualizadas: {len(rows)}")
print(f"CSV actualizado: {OUT_PATH}")
