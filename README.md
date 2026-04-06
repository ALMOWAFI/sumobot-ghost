# Sumo Bot CAD

This project uses `build123d` on Python 3.11 because it is available locally now, supports a code-first parametric workflow, and exports both `STEP` and `STL`.

## Project layout

- `src\` contains the CAD source
- `exports\` contains generated `STEP`, `STL`, and manifest files
- `tools\` contains automation scripts for FreeCAD
- `openscad\` contains the OpenSCAD preview scene
- `references\` contains the original design brief
- `references\sumobot_gap_matrix.md` compares this design against real external sumo-bot references
- `references\current_design_enhancement_brief.md` narrows those references into improvements for the current chassis
- `checklists\` contains the build and validation workflow
- `.venv\` contains the local Python environment

## Outputs

Run:

```powershell
.\run_export.ps1
```

Estimate assembled mass from the current CAD plus component assumptions:

```powershell
.\run_mass_estimate.ps1
```

Import the generated STEP into a native FreeCAD document:

```powershell
.\run_freecad_import.ps1
```

Generate an OpenSCAD preview PNG from the exported STL:

```powershell
.\run_openscad_preview.ps1
```

If the imported FreeCAD model opens but the viewport looks empty, use `View -> Fit all` once. The file contains a single imported solid body.

Generated files land in `exports\`:

- `sumobot_chassis.step`
- `sumobot_chassis.stl`
- `sumobot_chassis.FCStd`
- `sumobot_rear_skid.step`
- `sumobot_rear_skid.stl`
- `sumobot_ballast_insert.step`
- `sumobot_ballast_insert.stl`
- `sumobot_chassis_preview.png`
- `sumobot_chassis_manifest.json`
- `sumobot_mass_estimate.json`
- `sumobot_mass_estimate.md`
- `checklists\sumobot_validation_checklist.md`
- `checklists\sumobot_validation_log.csv`

## Explicit assumptions

- Chassis base footprint: `182 x 168 mm`.
- Actual overall envelope with switch guard: `188 x 168 mm`, still under the `220 x 220 mm` rule.
- Motor package: `TT DC gear motor`, `70 x 23 x 18 mm`.
- Remaining motor assumption: the TT shaft centerline is treated as `10.5 mm` above the motor mount floor.
- Wheel target: `65 mm` diameter, `26 mm` width.
- Battery package: `7.4V Li-ion`, `70 x 40 x 20 mm`.
- ESP32 mount: tray sized for `ESP32 DevKit V1`, `55 x 28 x 15 mm`.
- Power mount: tray sized for `LM2596`, `45 x 22 x 15 mm`.
- Front sensor support: `QTR-8RC` shelf and `VL53L0X` shelf are included.
- Front ballast support: mirrored ballast bays sit inside the front half behind the sensor deck.
- Ballast insert reference: [sumobot_ballast_insert.step](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\exports\sumobot_ballast_insert.step) is sized for `1/4 oz` steel wheel-weight segments, `5` segments per insert, `10` total across the robot.
- Switch slot: rear-access `KCD1` rocker-switch cutout, `19 x 13 mm`.
- Rear skid: two-hole `M3` mounting pattern on the rear bridge.

## Included features

- Integrated front wedge with a conservative nose height target of `1.5 mm`
- Left and right TT motor cradles with inner guides, end stops, and strap slots
- Battery bay with exact-fit rails and strap slots
- ESP32 DevKit V1 tray
- LM2596 tray
- QTR-8RC front shelf
- VL53L0X front shelf
- Paired internal ballast bays behind the front sensor deck
- Separate printable ballast insert sized for standard `1/4 oz` steel segments
- Shallow floor wire trenches linking motors, battery, ESP32, buck converter, and front sensors
- Small cable anchor slots for tidy zip-tie or thread lashing
- Dedicated motor lead pass-throughs and board-side wire pass windows
- ESP32 end-capture tabs plus an enlarged USB service pocket for programming cable access
- Adjustable LM2596 mounting slots in the tray floor for screw retention when the module hole pattern matches
- Battery side reliefs and a rear-left battery lead notch aimed into the power trench
- Inner board service reliefs so the ESP32 and LM2596 can be seated and removed without prying against full-height rails
- Sensor mounting slots for the QTR-8RC and VL53L0X shelves
- Guarded rocker-switch pocket with rear ribs and a top roof
- Separate low-profile rear skid wear part with slotted M3 mounting holes
- Rear switch slot
- Rear skid mount pattern

## Print notes

- Material: `PETG` for the first functional print. Move to nylon or CF-reinforced filament only after fit checks.
- Rear skid: print a temporary skid in `PETG`, but plan to remake [sumobot_rear_skid.step](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\exports\sumobot_rear_skid.step) in `PTFE` or `UHMW` for lower drag.
- Orientation: print the chassis floor-down so the wedge and wall geometry keep the assembly stable.
- Supports: likely only needed under the rear bridge and any especially aggressive wedge nose on your slicer profile.
- Infill: start around `35%` gyroid or cubic with `4 to 5` walls.
- Hardware: use `M3` fasteners, cable ties or hook-and-loop straps, and heat-set inserts only after confirming local wall thicknesses still match your chosen insert.

## Assembly order

1. Install the motors and route the leads through the side pass-throughs into the floor trenches.
2. Mount the rear skid wear part.
3. Place the battery and route its leads through the battery notch toward the buck converter zone.
4. Install the LM2596 and power wiring.
5. Install the ESP32 and keep the USB side aligned with the service pocket.
6. Mount the front sensors and pull their wires through the front sensor slot into the main trench.
7. Print `2x` ballast inserts and drop one into each ballast bay.
8. Start with `10x` standard `1/4 oz` steel wheel-weight segments total, `5` per insert, then drive-test before changing the load.

## Mass model

- The mass tool uses the actual CAD volume of the chassis and rear skid, then converts that volume into a PETG mass estimate.
- It also reports the printable ballast-insert mass and the standard `10`-segment steel loadout for the insert pair.
- It reports both a solid-PETG equivalent and a realistic printed range for the chassis.
- Component masses are a mix of vendor specs and explicit engineering allowances where your exact purchased part is still generic.
- The two biggest current mass uncertainties are the exact `65 mm` wheel variant and the exact `7.4 V` battery pack.
- The current electronics list still needs a locked motor-driver board, so the report includes a separate `TB6612`-class allowance instead of pretending that detail is fixed.
- The report also estimates how optional front ballast shifts the robot's x-axis center of mass.

## Short BOM

- `2x` TT DC gear motor
- `2x` `65 x 26 mm` TT wheel
- `1x` `7.4V Li-ion` battery
- `1x` `ESP32 DevKit V1`
- `1x` `LM2596` buck converter
- `1x` motor driver board, still to be locked
- `1x` `KCD1` rocker switch
- `1x` `QTR-8RC`
- `1x` `VL53L0X`
- `2x` printed ballast inserts
- `10x` standard `1/4 oz` steel wheel-weight segments
- `2x` M3 skid fasteners
- `6 to 10x` cable ties or hook-and-loop straps for battery, motors, and PCBs
