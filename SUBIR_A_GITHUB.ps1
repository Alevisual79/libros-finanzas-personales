# ============================================================
#  SUBIR PROYECTO A GITHUB — doble clic y listo
# ============================================================

$host.UI.RawUI.WindowTitle = "Subir a GitHub"
$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   SUBIR PROYECTO LIBROS IA A GITHUB" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Colecciones incluidas:" -ForegroundColor Yellow
Write-Host "  - Finanzas Personales: 101 libros (Metodo 5P)" -ForegroundColor Gray
Write-Host "  - Salud y Bienestar:   101 libros (Metodo RESET)" -ForegroundColor Gray
Write-Host ""

Set-Location "c:\Users\usuario\Desktop\IA\Libros"

Write-Host "Paso 1: Verificando estado del repositorio..." -ForegroundColor Yellow
$status = git status --short
if ($status) {
    Write-Host "  Hay cambios sin commitear:" -ForegroundColor Red
    Write-Host $status
    Write-Host ""
    Write-Host "  Haciendo commit de los cambios pendientes..." -ForegroundColor Yellow
    git add .
    git commit -m "Actualizar archivos pendientes"
}
else {
    Write-Host "  Repositorio limpio." -ForegroundColor Green
}

Write-Host ""
Write-Host "Paso 2: Subiendo commits a GitHub..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "   LISTO! Repositorio actualizado en:" -ForegroundColor Green
    Write-Host "   https://github.com/Alevisual79/libros-finanzas-personales" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
}
else {
    Write-Host ""
    Write-Host "  Error al subir. Intenta autenticarte primero:" -ForegroundColor Red
    Write-Host "  gh auth login" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Pulsa Enter para cerrar..." -ForegroundColor Gray
Read-Host
