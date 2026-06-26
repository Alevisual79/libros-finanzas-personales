"""
Borra todos los EPUBs existentes y los regenera desde cero
usando convert_to_epub.py con el CSS actualizado (texto justificado).
~30-40 minutos para 1,418 libros.
"""
import os, subprocess, sys, time

BASE = r"c:\Users\usuario\Desktop\IA\Libros"
COLLECTIONS = [
    "AI_Artificial_Intelligence", "Applied_Psychology", "Entrepreneurship",
    "Health_Wellness", "Personal_Finance", "Productivity_Success",
    "Relationships_Communication", "IA_Inteligencia_Artificial",
    "Psicologia_Aplicada", "Emprendimiento", "Salud_Bienestar",
    "Finanzas_Personales", "Productividad_Exito", "Relaciones_Comunicacion",
]

def delete_epubs():
    total = 0
    for col in COLLECTIONS:
        col_path = os.path.join(BASE, col)
        for root, _, files in os.walk(col_path):
            for f in files:
                if f.endswith(".epub"):
                    os.remove(os.path.join(root, f))
                    total += 1
    return total

def main():
    print("Borrando EPUBs existentes...")
    deleted = delete_epubs()
    print(f"  {deleted} EPUBs borrados.")

    print("\nRegenerando todos los EPUBs con CSS actualizado...")
    print("(~30-40 min — puedes ver el progreso abajo)\n")
    t0 = time.time()

    result = subprocess.run(
        [sys.executable, os.path.join(BASE, "convert_to_epub.py")],
        cwd=BASE
    )

    elapsed = int(time.time() - t0)
    if result.returncode == 0:
        print(f"\nListo en {elapsed//60}m {elapsed%60}s.")
    else:
        print(f"\nAlgun error en la regeneracion (returncode={result.returncode}).")

if __name__ == "__main__":
    main()
