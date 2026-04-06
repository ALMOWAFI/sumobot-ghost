$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$Script = Join-Path $ProjectRoot "tools\estimate_mass.py"

if (-not (Test-Path -LiteralPath $Python)) {
    throw "Python not found at $Python"
}

& $Python $Script
