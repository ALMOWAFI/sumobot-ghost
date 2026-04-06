$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$openscad = "C:\Program Files\OpenSCAD\openscad.exe"
$scad = Join-Path $projectRoot "openscad\sumobot_chassis_preview.scad"
$outputPng = Join-Path $projectRoot "exports\sumobot_chassis_preview.png"

& $openscad `
  --autocenter `
  --viewall `
  --projection=ortho `
  --imgsize=1600,1200 `
  --colorscheme=Tomorrow `
  -o $outputPng `
  $scad
