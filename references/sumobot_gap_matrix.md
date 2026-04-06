# Sumo Bot Gap Matrix

This compares the current chassis against representative `1 kg` sumo references and turns the comparison into decisions.

Current project references:

- source CAD: [sumobot_chassis.py](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\src\sumobot_chassis.py)
- mass model: [sumobot_mass_estimate.md](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\exports\sumobot_mass_estimate.md)
- validation workflow: [sumobot_validation_checklist.md](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\checklists\sumobot_validation_checklist.md)

Reference designs:

- Cytron `1KG Autonomous Sumo Robot using URC10`
  <https://www.cytron.io/tutorial/1-kg-autonomous-sumo-robot-starter-kit-user-guide-using-urc10>
- JSumo `BB1 Midi Sumo Robot`
  <https://www.jsumo.com/bb1-midi-sumo-robot-kit-assembled>
- `Mini-Sumo Robot Design with Respect to the Control System`
  <https://www.researchgate.net/publication/364052980_Mini-Sumo_Robot_Design_with_Respect_to_the_Control_System>

## Current Design Snapshot

- outer envelope: `188 x 168 x 32 mm`
- current estimated assembled mass: `377.68 to 456.06 g`
- with `TB6612` and standard `70 g` insert load: `452.94 to 533.24 g`
- drivetrain assumption: `TT DC gear motor`, `65 x 26 mm` TT wheels
- front ballast strategy: internal paired bays and inserts for `10` standard `1/4 oz` steel segments

Source:
- [sumobot_mass_estimate.md](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\exports\sumobot_mass_estimate.md)

## Reference Snapshot

### Cytron URC10

- `under 1 kg`
- `under 15 x 15 cm`
- `12V 580 RPM 3.5 kgfcm` geared motors
- `43 x 30 mm` silicone wheels
- `copper base`
- front-mounted sensors and front-driven packaging

This is a compact, dense, traction-first architecture.

### JSumo BB1

- `150 x 135 x 55 mm`
- `870 g` with battery
- `39 x 11 mm` high-friction wheels
- `25 mm` motors
- much denser packaging than our current robot

This is closer to a mature `1 kg` competition package than a student prototype.

### Research Paper Robot

- `4 mm` aluminum base
- front wedge built into the base
- line sensors in the front of the base
- opponent sensors close to the front
- PCB protected inside the body

This confirms the structural pattern used by serious bots: dense base, protected internals, front-dominant attack geometry.

## Gap Matrix

| Area | Our Design | Reference Pattern | Gap | Decision |
|---|---|---|---|---|
| Drivetrain power | TT motors, assumed shaft datum | stronger geared motors, roughly `25 mm` class or better | very large | change later with upgraded motors |
| Wheel strategy | `65 x 26 mm` TT wheels | smaller high-grip wheels, often silicone, around `39-43 mm` | very large | change later with upgraded wheels |
| Weight level | `378-456 g` bare system, `453-533 g` with standard ballast load | many strong `1 kg` bots are much denser, often near class limit | large | tune now with ballast, but full jump waits for drivetrain upgrade |
| Front load path | printed wedge integrated into plastic shell | copper or aluminum base and wedge, front structure carries the fight load | large | improve later with metal front/base interface |
| Sensor zone | forward sensor deck, now placed more correctly | sensors very close to front and integrated tightly into attack module | medium | validate now, refine after physical checks |
| Wheel exposure | wheel windows are functional but still fairly open | wheel sidewalls protected where possible | medium | change now after first real fit check |
| Motor retention | guides, stops, straps | positive retention on real motor geometry | medium to large | change now after real motor measurement |
| Battery retention | reasonable rails and straps | compact, dense, impact-tolerant package | medium | change now only if physical test shows movement |
| Wiring discipline | trenches, pass-throughs, anchors are present | clean, protected routing under dense packaging | small to medium | keep and validate now |
| Rear support | replaceable skid concept exists | replaceable low-friction skid or rear support is standard | small | keep now, improve material later |
| Serviceability | decent for a prototype | serious bots still preserve access to battery, programming, and sensors | small | keep |
| CAD source of truth | strong parametric script | reference bots vary, but geometry intent is usually mature | small | keep |

## What To Keep

- the current parameterized source in [sumobot_chassis.py](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\src\sumobot_chassis.py)
- the split zones for battery, ESP32, power, sensors, and switch
- the wiring trenches and service openings
- the replaceable rear skid concept
- the internal ballast system and insert approach

These are not the weak parts of the design.

## Change Now

### 1. Motor certainty

The most important immediate fix is to stop relying on the shaft-height assumption at [sumobot_chassis.py#L39](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\src\sumobot_chassis.py#L39).

Reason:
- if axle height is wrong, wheel contact and wedge behavior are wrong

Action:
- measure the real TT motor
- tighten the motor cradle around the real body and gearbox
- add anti-twist geometry, not only straps

### 2. Wheel protection

The wheel windows at [sumobot_chassis.py#L454](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\src\sumobot_chassis.py#L454) should be reduced after the first real fit check.

Reason:
- exposed wheel sidewalls are easy to attack

Action:
- keep only the clearance the real wheel needs

### 3. Sensor and front module validation

The front sensor deck around [sumobot_chassis.py#L374](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\src\sumobot_chassis.py#L374) is directionally right but still unproven.

Reason:
- front height and protection matter more than visual style

Action:
- verify QTR height
- verify VL53 sight line
- verify front impacts do not hit sensor hardware first

### 4. Ballast tuning

The current ballast system is useful because it lets us test `0 g`, `35 g`, and `70 g` instead of redesigning by instinct.

Source:
- [sumobot_mass_estimate.md](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\exports\sumobot_mass_estimate.md)

Action:
- keep the insert system
- test before adding more mass

## Change Later

### 1. Wheels

Serious bots converge on smaller, grippier wheels:
- Cytron uses `43 x 30 mm` silicone wheels
- JSumo uses `39 x 11 mm` high-friction wheels

Our `65 mm` TT wheels are a temporary packaging choice, not an end-state competitive choice.

### 2. Motors

TT motors are too weak for a near-`1 kg` pushing robot.

The SunFounder TT reference is only `0.8 kg.cm` stall torque at `6V`, while Cytron uses `3.5 kgfcm` motors and JSumo uses a much stronger `25 mm` motor class.

Reference:
- <https://docs.sunfounder.com/projects/3in1-kit-v2/en/latest/components/component_tt_motor.html>

### 3. Front structural material

The references repeatedly use metal in the load path:
- Cytron: copper base
- paper robot: `4 mm` aluminum base

So the long-term winning design should likely use:
- a metal front plate
- or a metal base with printed upper packaging

## Decision Summary

### Keep

- packaging architecture
- wiring strategy
- ballast concept
- skid concept

### Fix now

- motor datum and retention
- wheel exposure
- front sensor validation
- ballast test sequence

### Postpone until upgraded hardware arrives

- complete drivetrain architecture
- final wheel size and compound
- final mass target near the top of the class
- metal front/base structure

## Practical Conclusion

The internet references confirm that our current robot should be treated as a correct prototype chassis for the current parts, not as the final winning architecture.

That is not a failure.

It means the correct next task is:

1. validate the current prototype against real parts
2. fix the geometry errors that physical testing exposes
3. reserve the real competitive jump for the upgraded motors and wheels
