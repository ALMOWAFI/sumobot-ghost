# Sumo Robot - Print Instructions

## Overview
This folder contains 13 STL files split into 3 groups.
Each group has different print settings.
Do NOT print "sumo completo.stl" — that is just a preview file.

---

## Group 1 — `1_GEARS_fine` (4 files)
These are the mechanical gears. They carry the most stress during the competition.
Print these with the highest quality.

| Setting | Value |
|---|---|
| Material | PETG |
| Layer height | 0.1 mm |
| Infill | 80% |
| Walls/Perimeters | 4 |
| Supports | No |
| Quantity | Print each file once (x2 and x4 are already in the filename) |

Files:
- PiñonMotorx2.stl
- PiñonPuentex2.stl
- PiñonLlantax2.stl
- EjePiñonPuente.stl

---

## Group 2 — `2_CHASSIS_normal` (6 files)
These are the main body and housing parts.

| Setting | Value |
|---|---|
| Material | PETG |
| Layer height | 0.2 mm |
| Infill | 40% |
| Walls/Perimeters | 4 |
| Supports | Only if needed (check slicer preview) |
| Quantity | Print each file once |

Files:
- CarcasaBase.stl
- CarcasaMedia.stl
- CarcasaTraccionCentral.stl
- CarcasaTraccionDer.stl
- CarcasaTraccionIz.stl
- TapaSumo.stl

---

## Group 3 — `3_SUPPORT_parts` (3 files)
These are the wheels, washers, and motor support arms.

| Setting | Value |
|---|---|
| Material | PETG |
| Layer height | 0.15 mm |
| Infill | 60% |
| Walls/Perimeters | 4 |
| Supports | No |
| Quantity | Print each file once (x2 and x4 are already in the filename) |

Files:
- llanta.stl
- BrazoMotorSoportex2.stl
- Arandelasx4.stl

---

## Robot Name — GHOST Text

The file `2_CHASSIS_normal/TapaSumo_GHOST.stl` is the lid with **GHOST engraved directly into the top surface** — ready to print as one piece, no extra steps needed.

Use `TapaSumo_GHOST.stl` instead of `TapaSumo.stl`. Same print settings as Group 2.

---

## General Notes
- Use PETG for all parts — do NOT use PLA (too brittle for competition)
- Keep the gear tolerances tight — gears must mesh smoothly
- Do not scale any part — print at 100% original size
- If PETG is unavailable, ABS is acceptable as a fallback
