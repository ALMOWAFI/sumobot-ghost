# Sumo Bot CAD Master Brief

Research date: 2026-04-06

## Tool Recommendation

For a code-first robot chassis project, the current practical choices are:

1. `build123d` as the primary scripted CAD option
   - Good fit when you want parametric CAD-as-code with modern Python structure.
   - Built on Open Cascade and positioned for precise CAD modeling and export.
   - Best when the machine has Python `>= 3.10`.
   - Official docs: <https://build123d.readthedocs.io/>
   - Repo: <https://github.com/gumyr/build123d>

2. `CadQuery` as the strongest mature alternative
   - Also code-first and based on Open Cascade.
   - Very good when you need robust `STEP` and `STL` export from Python scripts.
   - Good choice if Codex finds CadQuery easier to install on the target machine.
   - Docs: <https://cadquery.readthedocs.io/>
   - Repo: <https://github.com/CadQuery/cadquery>

3. `FreeCAD` as the GUI companion, not the first modeling choice
   - Best for visual inspection, manual tweaking, checking clearances, and validating exports.
   - Strong for interactive parametric CAD and `STEP` workflows.
   - Site/repo: <https://github.com/FreeCAD/FreeCAD>

4. `OpenSCAD` as the lightweight fallback
   - Best when you need a fast, low-friction scripted path to a printable `STL`.
   - Less ideal than OCCT-based tools for richer mechanical CAD and `STEP` workflows.
   - Docs: <https://openscad.org/documentation.html>
   - Repo: <https://github.com/openscad/openscad>

## Recommended Stack For This Project

Use this priority order:

1. Try `build123d`
2. If that is blocked, use `CadQuery`
3. Use `FreeCAD` for inspection or final manual adjustment
4. Fall back to `OpenSCAD` only if the environment is too constrained

Reason:
- This robot needs a real mechanical workflow, not just a printable shape.
- You want editable dimensions, motor mounts, battery bay, switch slot, and exportable CAD.
- `STEP` matters if you will iterate later or hand the design to someone else.

## Competition Constraints

Competition: Makers Club Sumo Bot Challenge
Date: April 11, 2026
Location: Constructor University
Event page: <https://www.makersclubcub.com/#/sumobot-event>

Verified constraints from the event page:
- Robot must be `remote-controlled`, not autonomous
- Team must build both the robot and the controller
- Maximum robot size: `22 cm x 22 cm`
- Maximum robot weight: `1 kg`
- Battery powered only
- Must include an on/off button
- Arena diameter: `140 cm`
- Arena surface: smooth `MDF`
- Border rings: `5 cm` colored border rings
- Arena height: `20 cm`
- Match format: best of 3 rounds
- Round duration: `3 minutes`
- Win condition: push opponent out of the ring
- Overtime: shrinking circle
- Not allowed: projectiles, flames, liquids, nets, entanglement devices, EMP/tasers, sharp cutting edges, arena-damaging features

## Mechanical Direction

Use these defaults unless better measured parts are available:

- Drivetrain: `2-wheel differential drive`
- Left wheel: one powered wheel
- Right wheel: one powered wheel
- Rear support: single skid or rear slider
- Front: low wedge/plow for pushing
- Printed chassis: yes
- Wheel traction: TPU, rubber sleeve, silicone sleeve, or O-rings
- Chassis target envelope: `20 cm x 20 cm` to leave inspection tolerance
- Weight distribution: front-heavy, about `55% to 60%` on the front
- Wheel diameter target: `55 to 65 mm`
- Wheel width target: `18 to 25 mm`
- Wedge angle target: `15 to 20 degrees`
- Front ground clearance target: `1 to 2 mm`
- Battery low and forward-middle
- Motors low and rigidly mounted
- Electronics center or rear-center
- Switch accessible from top or rear

## Electronics Assumptions

- Bot MCU: `ESP32-WROOM-32`
- Motor driver: `TB6612FNG`
- Battery: `2S LiPo 7.4V`
- Buck converter for logic rail if needed
- Controller MCU: `ESP32-C3` or another ESP32-class controller
- Wireless link: `ESP-NOW`
- Controller input: two joysticks
- Optional edge sensors later, so leave mounting space at the front and rear

## Expected Deliverables

- Parametric chassis CAD source
- `STL` export
- `STEP` export if supported by the chosen toolchain
- Mounting features for:
  - motors
  - battery
  - ESP32
  - TB6612FNG
  - on/off switch
  - rear skid
- Front wedge or wedge-ready mount
- Short hardware BOM
- Print orientation notes
- Material recommendation

## Acceptance Criteria

The first version is acceptable if it:

- fits within `22 cm x 22 cm`
- is designed around a realistic `1 kg` sumo bot
- is clearly editable through named parameters
- has assembly access for battery and electronics
- can be exported to at least `STL`
- preferably exports `STEP`
- avoids banned sharp weapon-like geometry

## Copy-Paste Prompt For Codex

```text
Act as a robotics CAD and fabrication-oriented coding agent.

I need a real, editable CAD-as-code workflow for a competition sumo robot chassis.

First, inspect the machine and choose the best currently available CAD stack using this priority:
1. build123d
2. CadQuery
3. FreeCAD as GUI companion
4. OpenSCAD fallback

If multiple options are available, prefer the one that best supports parametric modeling plus both STEP and STL export.
Do not pick blindly. State which stack you chose and why.

Project:
Design a 3D-printable remote-controlled sumo robot chassis and generate fabrication files.

Competition:
Makers Club Sumo Bot Challenge
Date: April 11, 2026
Location: Constructor University

Verified rules and constraints:
- Robot must be remote-controlled, not autonomous
- Team must build both the robot and the controller
- Maximum robot size: 22 cm x 22 cm
- Maximum robot weight: 1 kg
- Battery powered only
- Must include an on/off button
- Arena diameter: 140 cm
- Arena surface: smooth MDF
- Border rings: 5 cm colored border rings
- Arena height: 20 cm
- Match format: best of 3 rounds
- Round duration: 3 minutes
- Victory: push opponent out of the ring
- Overtime: shrinking circle
- Not allowed: projectiles, flames, liquids, nets, entanglement devices, EMP/tasers, sharp cutting edges, or arena-damaging features

Design direction:
- 2-wheel differential drive
- One powered wheel on the left and one on the right
- Rear skid or rear slider
- Front wedge/plow for pushing
- 3D-printable chassis
- Low center of gravity
- Front-heavy weight distribution
- Wheels should use rubber, TPU, silicone sleeve, or O-rings for traction
- Target envelope around 20 cm x 20 cm to leave inspection tolerance
- Easy to assemble and service

Electronics assumptions:
- Bot MCU: ESP32-WROOM-32
- Motor driver: TB6612FNG
- Battery: 2S LiPo 7.4V
- Buck converter for logic rail if needed
- Controller MCU: ESP32-C3 or similar ESP32-based controller
- Wireless link: ESP-NOW
- Two-joystick controller
- Optional edge sensors later, so leave room for them

Mechanical defaults:
- Wheel diameter target: 55 to 65 mm
- Wheel width target: 18 to 25 mm
- Wedge angle target: 15 to 20 degrees
- Front ground clearance target: 1 to 2 mm
- Battery low and forward-middle
- Motors low and rigidly mounted
- Electronics center or rear-center
- Switch accessible from top or rear

Required tasks:
1. Inspect installed tools and Python version
2. If needed, install the lightest practical CAD toolchain that can support this job
3. Create a parametric chassis model with named dimensions
4. Include motor mounts, battery bay, ESP32 mount, TB6612FNG mount, switch slot, and rear skid mount
5. Include either an integrated front wedge or a wedge-ready mount
6. Export STL
7. Export STEP if the chosen stack supports it
8. Save the source CAD script
9. Explain all assumptions explicitly
10. Prefer a working first version over perfect styling

Deliverables:
- CAD source file
- STL export
- STEP export if supported
- Short BOM for screws, inserts, and mounting hardware
- Print notes including material, orientation, and any support recommendations

Important constraints:
- Do not silently guess critical dimensions if a better explicit assumption is available
- If an exact motor or battery size is unknown, choose a common practical option and state it clearly
- Preserve parametric editability
- Keep the design legal under the event rules
```

## Suggested Repo Shortlist

If Codex wants current primary sources, use these first:

- build123d: <https://github.com/gumyr/build123d>
- build123d docs: <https://build123d.readthedocs.io/>
- CadQuery: <https://github.com/CadQuery/cadquery>
- CadQuery docs: <https://cadquery.readthedocs.io/>
- FreeCAD: <https://github.com/FreeCAD/FreeCAD>
- OpenSCAD: <https://github.com/openscad/openscad>

## Practical Decision Summary

If the main laptop has:

- Python `>= 3.10` and package install works:
  - prefer `build123d`

- Python `3.9` to `3.12` and a solid OCCT-based scripting path is needed:
  - `CadQuery` is a very good default

- a constrained environment or you only need a fast printable shell:
  - `OpenSCAD`

- a need for direct visual editing and manual CAD inspection:
  - keep `FreeCAD` available too
