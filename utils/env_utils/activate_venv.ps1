$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

.\venv\Scripts\Activate.ps1

$env:PYTHONPATH = "$projectRoot;$env:PYTHONPATH"

Write-Host "Virtual environment activated with project root in PYTHONPATH"
Write-Host "Project root: $projectRoot"
