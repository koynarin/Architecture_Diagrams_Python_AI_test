# Run the Contoso architecture diagram generator
# Usage: .\run.ps1

$scriptPath = Join-Path $PSScriptRoot "contoso_architecture_diagram.py"

if (-not (Test-Path $scriptPath)) {
    Write-Error "Diagram script not found: $scriptPath"
    exit 1
}

Write-Host "Running Contoso architecture diagram generator..."
python $scriptPath

if ($LASTEXITCODE -ne 0) {
    Write-Error "Diagram generation failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

Write-Host "Done. Check diagrams/ for generated PNG, DOT, and DRAWIO files."
