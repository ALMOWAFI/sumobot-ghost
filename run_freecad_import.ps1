$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$freecadPython = "C:\Users\almwa\AppData\Local\Programs\FreeCAD 1.1\bin\python.exe"
$script = Join-Path $projectRoot "tools\freecad_import_step.py"
$inputStep = Join-Path $projectRoot "exports\sumobot_chassis.step"
$outputFcstd = Join-Path $projectRoot "exports\sumobot_chassis.FCStd"

& $freecadPython $script $inputStep $outputFcstd
