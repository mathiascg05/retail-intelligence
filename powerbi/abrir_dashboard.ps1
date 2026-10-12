# Apunta el parametro CarpetaDatos a data\powerbi de este repositorio y abre el dashboard.
$aqui = $PSScriptRoot
$datos = (Resolve-Path (Join-Path $aqui '..\data\powerbi')).Path.TrimEnd('\') + '\'
$tmdl = Join-Path $aqui 'RetailIntelligence.SemanticModel\definition\expressions.tmdl'
$texto = [IO.File]::ReadAllText($tmdl)
$nuevo = [regex]::Replace($texto, 'expression CarpetaDatos = "[^"]*"', { param($m) 'expression CarpetaDatos = "' + $datos + '"' })
[IO.File]::WriteAllText($tmdl, $nuevo, (New-Object Text.UTF8Encoding $false))
Write-Host "Datos: $datos"
Start-Process (Join-Path $aqui 'RetailIntelligence.pbip')
