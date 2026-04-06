# Current Design Enhancement Brief

This brief answers one question:

How do we improve the current chassis by learning from stronger external sumo-bot designs, without throwing away the architecture we already have?

Related files:

- gap matrix: [sumobot_gap_matrix.md](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\references\sumobot_gap_matrix.md)
- source CAD: [sumobot_chassis.py](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\src\sumobot_chassis.py)
- mass model: [sumobot_mass_estimate.md](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\exports\sumobot_mass_estimate.md)

## Principle

Do not copy internet shapes.

Copy the design logic that strong bots share:

- dense front half
- protected wheels
- low, stiff attack geometry
- protected sensors
- compact, controlled mass distribution
- minimal exposed weak points

## Enhancements We Can Apply To The Current Design

### 1. Keep the front edge clean and make the attack module denser

Current geometry:
- wedge at [sumobot_chassis.py#L282](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\src\sumobot_chassis.py#L282)
- front sensor deck at [sumobot_chassis.py#L384](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\src\sumobot_chassis.py#L384)
- internal ballast bays at [sumobot_chassis.py#L400](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\src\sumobot_chassis.py#L400)

Enhancement:
- keep ballast behind the sensor deck, not in the nose
- keep sensors close to the front, but not proud of the wedge
- avoid any openings or cosmetic cutouts in the front half that are not doing real work

Why:
- the references all converge on a front-dominant architecture
- the nose should push, not expose parts

Status:
- mostly already aligned
- needs physical validation, not conceptual change

### 2. Reduce wheel exposure after real fit is confirmed

Current geometry:
- wheel windows at [sumobot_chassis.py#L452](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\src\sumobot_chassis.py#L452)

Enhancement:
- shrink the wheel opening to the minimum real clearance
- keep a protective rim or wall around the opening
- avoid exposing the sidewall more than needed for wheel rotation

Why:
- stronger bots try to protect the wheel sidewall from side contact
- this is one of the easiest current-design improvements once real fit is verified

Status:
- should be changed after the first real motor/wheel fit check

### 3. Turn the motor area from strap retention into shape retention

Current geometry:
- motor guides and end stops at [sumobot_chassis.py#L305](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\src\sumobot_chassis.py#L305)
- strap slots at [sumobot_chassis.py#L438](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\src\sumobot_chassis.py#L438)

Enhancement:
- add anti-rotation features keyed to the real TT gearbox shape
- use the strap as secondary retention, not primary retention
- tighten the stop geometry around the actual motor body once measured

Why:
- the references use more serious drivetrain retention than a generic strap cradle
- if the motor shifts, the whole robot becomes inconsistent

Status:
- highest-priority geometry enhancement for the current hardware

### 4. Prepare a future hard front load path without redesigning the shell

Current geometry:
- wedge is fully plastic in [sumobot_chassis.py#L282](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\src\sumobot_chassis.py#L282)

Enhancement:
- reserve or add a simple mounting interface for a future metal front shoe or plate
- do not redesign around metal yet
- just make the current chassis ready for that later upgrade

Why:
- the strongest reference bots repeatedly use copper or aluminum in the front/base load path
- this gives us a clean migration path instead of starting over later

Status:
- beneficial now
- not urgent before drivetrain fit is validated

### 5. Make the battery zone more collision-stable

Current geometry:
- battery tray at [sumobot_chassis.py#L329](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\src\sumobot_chassis.py#L329)
- battery relief and notch features at [sumobot_chassis.py#L542](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\src\sumobot_chassis.py#L542)

Enhancement:
- if physical tests show movement, add harder fore-aft stops
- optionally add a thin compression pad zone
- keep removal serviceable

Why:
- reference bots are compact and dense, so heavy parts do not get to slide around

Status:
- only change after physical movement is observed

### 6. Protect the sensors with geometry, not just careful placement

Current geometry:
- QTR mount slots at [sumobot_chassis.py#L728](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\src\sumobot_chassis.py#L728)
- VL53 mount slots at [sumobot_chassis.py#L742](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\src\sumobot_chassis.py#L742)

Enhancement:
- add shallow protective side cheeks or local shielding if the sensors are exposed
- do not block the field of view or line-sensing geometry

Why:
- good bots keep front sensors close, but not sacrificial

Status:
- depends on real assembly and sightline checks

### 7. Use ballast as tuning, not as compensation for weak architecture

Current mass model:
- [sumobot_mass_estimate.md](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\exports\sumobot_mass_estimate.md)

Enhancement:
- keep the insert system
- treat `0 g`, `35 g`, and `70 g` as test points
- do not chase maximum class mass with TT motors

Why:
- stronger reference bots can exploit higher mass because they also have stronger motors and better wheels
- current hardware does not justify blindly adding more weight

Status:
- already the correct strategy

## Enhancements We Should Not Pretend To Do Now

These are reference-inspired, but they are not honest current-design optimizations for the present hardware:

- switching to final small silicone wheels before the upgraded wheels arrive
- redesigning around a heavy near-`1 kg` package with TT motors
- fully metalizing the front structure before drivetrain geometry is settled
- copying the exact external silhouette of Cytron or JSumo bots

## Best Enhancement Order

1. measure real TT motor and refine retention
2. confirm axle height and wheel opening alignment
3. minimize wheel exposure
4. validate sensor height and protection
5. test ballast at `0 g`, `35 g`, `70 g`
6. add a future metal front-shoe interface
7. only then consider deeper structural changes

## Bottom Line

The references do not tell us to abandon the current chassis.

They tell us exactly where to tighten it:

- drivetrain certainty
- wheel protection
- front-module discipline
- controlled ballast
- upgrade path toward a stiffer front load path

That is how we improve what we already have without wasting work.
