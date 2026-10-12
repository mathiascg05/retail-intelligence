# Trae la ultima version del repositorio, apunta el parametro CarpetaDatos
# a data\powerbi de este repositorio y abre el dashboard en Power BI Desktop.
$aqui = $PSScriptRoot
$raiz = (Resolve-Path (Join-Path $aqui '..')).Path
$tmdl = Join-Path $aqui 'RetailIntelligence.SemanticModel\definition\expressions.tmdl'

if (Get-Process -Name 'PBIDesktop' -ErrorAction SilentlyContinue) {
    Write-Host 'Power BI Desktop esta abierto. Cierralo sin guardar y vuelve a ejecutar este archivo.' -ForegroundColor Yellow
    Read-Host 'Pulsa Enter para salir'
    exit 1
}

# 1. Actualizar el repositorio (si hay git)
if ((Get-Command git -ErrorAction SilentlyContinue) -and (Test-Path (Join-Path $raiz '.git'))) {
    Push-Location $raiz
    git checkout -- 'powerbi/RetailIntelligence.SemanticModel/definition/expressions.tmdl' 2>$null
    Write-Host 'Buscando la ultima version...'
    git pull --ff-only
    if ($LASTEXITCODE -ne 0) {
        Write-Host 'No se pudo actualizar (sin internet o sin sesion en GitHub). Se abre la version local.' -ForegroundColor Yellow
    }
    Write-Host ('Version: ' + (git log -1 --format='%h %s (%ad)' --date=short)) -ForegroundColor Green
    Pop-Location
} else {
    Write-Host 'Git no esta disponible: se abre la version local sin actualizar.' -ForegroundColor Yellow
}

# 2. Apuntar CarpetaDatos a los CSV de este repositorio
$datos = (Resolve-Path (Join-Path $raiz 'data\powerbi')).Path.TrimEnd('\') + '\'
$texto = [IO.File]::ReadAllText($tmdl)
$nuevo = [regex]::Replace($texto, 'expression CarpetaDatos = "[^"]*"', { param($m) 'expression CarpetaDatos = "' + $datos + '"' })
[IO.File]::WriteAllText($tmdl, $nuevo, (New-Object Text.UTF8Encoding $false))
Write-Host "Datos: $datos"

# 3. Abrir el dashboard
Start-Process (Join-Path $aqui 'RetailIntelligence.pbip')
Write-Host 'Abriendo Power BI... cuando cargue, pulsa Actualizar.'
Start-Sleep -Seconds 4
