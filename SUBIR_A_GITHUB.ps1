# ============================================================
#  SUBIR PROYECTO A GITHUB — doble clic y listo
# ============================================================

$host.UI.RawUI.WindowTitle = "Subir a GitHub"
$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User")

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   SUBIR PROYECTO LIBROS IA A GITHUB" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Paso 1: Iniciando sesion en GitHub..." -ForegroundColor Yellow
Write-Host "(Se abrira el navegador - haz clic en 'Authorize GitHub CLI')" -ForegroundColor Gray
Write-Host ""

gh auth login --hostname github.com --git-protocol https --web

Write-Host ""
Write-Host "Paso 2: Obteniendo tu usuario de GitHub..." -ForegroundColor Yellow
$usuario = gh api user --jq .login
Write-Host "  Usuario: $usuario" -ForegroundColor Green

Write-Host ""
Write-Host "Paso 3: Creando repositorio 'libros-finanzas-personales'..." -ForegroundColor Yellow
gh repo create libros-finanzas-personales --public --description "Serie de 101 libros de finanzas personales - El Metodo 5P" 2>&1
Write-Host "  Repositorio creado." -ForegroundColor Green

Write-Host ""
Write-Host "Paso 4: Preparando archivos..." -ForegroundColor Yellow
Set-Location "c:\Users\usuario\Desktop\IA\Libros"
git init
git config user.email "aepp1979@gmail.com"
git config user.name "$usuario"
git add .
git commit -m "Proyecto inicial: 101 libros de finanzas personales - El Metodo 5P"

Write-Host ""
Write-Host "Paso 5: Subiendo a GitHub..." -ForegroundColor Yellow
git branch -M main
git remote add origin "https://github.com/$usuario/libros-finanzas-personales.git"
git push -u origin main

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "   LISTO! Tu proyecto esta en GitHub:" -ForegroundColor Green
Write-Host "   https://github.com/$usuario/libros-finanzas-personales" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Pulsa Enter para cerrar..." -ForegroundColor Gray
Read-Host
