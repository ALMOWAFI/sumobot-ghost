# Sumo Bot Validation Checklist

Use this after printing the chassis and before changing geometry again.

The goal is simple:

- verify the current design against the real hardware
- find the first true mechanical failures
- avoid redesigning from guesses

## Tools

- caliper
- ruler
- kitchen scale or small digital scale
- marker
- tape
- cable ties or straps
- notebook or the log file in `checklists\sumobot_validation_log.csv`

## Rule Check

- [ ] Outer envelope is still under `220 x 220 mm`
- [ ] Power switch is reachable
- [ ] Front edge is low but not sharp or destructive
- [ ] Total robot mass is under `1000 g`

Record:

- overall length:
- overall width:
- overall height:
- assembled mass:

## Print Check

- [ ] Chassis printed flat without major warp
- [ ] Wedge nose is not curled upward
- [ ] Rear bridge is not sagged or cracked
- [ ] Ballast bays printed cleanly
- [ ] Ballast inserts fit their bays without forcing
- [ ] Skid holes line up with the rear bridge

Record:

- chassis print mass:
- skid print mass:
- ballast insert mass each:

## Motor Fit

Related model assumptions:
- TT motor size in [sumobot_chassis.py](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\src\sumobot_chassis.py): [motor params](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\src\sumobot_chassis.py#L31)

- [ ] Left motor drops into its cradle without trimming
- [ ] Right motor drops into its cradle without trimming
- [ ] Each motor sits flat on the floor
- [ ] Front and rear motor stops actually stop the motor body
- [ ] Strap path clears the motor body and gearbox
- [ ] Motor cannot twist significantly by hand once strapped
- [ ] Motor wires pass through the side openings without pinching

Record:

- measured motor body:
- measured shaft center from mount floor:
- left motor fit notes:
- right motor fit notes:

## Wheel and Ground Contact

- [ ] Wheels mount fully on the shafts
- [ ] Wheels spin without rubbing the chassis wall
- [ ] Wheel openings are centered on the actual axle line
- [ ] Both drive wheels touch the floor evenly
- [ ] Rear skid touches lightly and does not lift a drive wheel
- [ ] Robot sits stable without rocking

Record:

- wheel diameter:
- wheel width:
- ground clearance at wedge:
- skid contact notes:

## Battery and Power Zone

Related model assumptions:
- battery and switch zone in [sumobot_chassis.py](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\src\sumobot_chassis.py#L46)

- [ ] Battery drops into the bay without forcing
- [ ] Battery can be removed without full disassembly
- [ ] Battery leads exit through the notch cleanly
- [ ] Battery does not slide fore-aft once strapped
- [ ] Switch snaps or seats into the rear cutout correctly
- [ ] Switch guard does not block finger access
- [ ] Power wires do not sit above the wheel plane

Record:

- measured battery size:
- battery fit notes:
- switch fit notes:

## ESP32, Driver, and Wiring

- [ ] ESP32 sits in its tray without bowing the board
- [ ] USB cable can be inserted without hitting the wall
- [ ] LM2596 sits flat in its tray
- [ ] Driver board location is defined and serviceable
- [ ] Main power wiring can be routed without crossing moving parts
- [ ] Wire trenches are actually useful and not too shallow
- [ ] Cable anchors are reachable and worth using

Record:

- ESP32 fit notes:
- LM2596 fit notes:
- driver board used:
- wiring notes:

## Sensors

Related front geometry:
- QTR and VL53 mounts in [sumobot_chassis.py](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\src\sumobot_chassis.py#L107)

- [ ] QTR-8RC physically fits the front mount
- [ ] QTR height above the floor is suitable for ring sensing
- [ ] VL53 fits its mount
- [ ] Sensor wiring can pass rearward without snagging
- [ ] Wedge and front lip do not block the intended sensing direction
- [ ] Sensors are protected enough that a small front impact will not hit them first

Record:

- QTR fit notes:
- VL53 fit notes:
- sensor height notes:

## Ballast

Related files:
- ballast insert model: [sumobot_ballast_insert.step](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\exports\sumobot_ballast_insert.step)
- ballast assumptions: [sumobot_mass_estimate.md](C:\Users\almwa\OneDrive%20-%20Constructor%20University\Desktop\sumobot-cad\exports\sumobot_mass_estimate.md)

- [ ] Both ballast inserts fit their bays
- [ ] Weight segments fit the insert slots
- [ ] Insert can be removed without damage
- [ ] Ballast stays low and does not interfere with sensors or battery
- [ ] Start with `0 g`, then `35 g`, then `70 g`

Record:

- ballast material:
- ballast mass installed:
- fit notes:

## Static Functional Checks

- [ ] Robot rolls straight when pushed by hand
- [ ] Wheels do not rub under side load
- [ ] Switch remains reachable with everything installed
- [ ] No wire can touch a wheel
- [ ] No board can shift under hand shock
- [ ] Rear skid is replaceable without full teardown

Record:

- static issues found:

## Drive Tests

Run on a flat safe floor first, not on the sumo ring.

- [ ] Low-speed forward drive is straight enough
- [ ] Low-speed reverse drive is controllable
- [ ] Full-turn left and right do not cause wheel rubbing
- [ ] Hard acceleration does not throw the battery or ballast
- [ ] Fast stop does not shift components
- [ ] Motors do not overheat unusually during a short test

Record:

- low-speed notes:
- turning notes:
- heat notes:

## Push Tests

Use a simple repeatable target first:
- a loaded box
- a rubber block
- another passive robot chassis

Test in this order:

1. no ballast
2. `35 g` ballast
3. `70 g` ballast

For each load:

- [ ] Robot keeps traction when pushing
- [ ] Wheels spin less than before or at least not more
- [ ] Nose stays low and does not ride up badly
- [ ] Rear skid drag stays acceptable
- [ ] Motors remain usable after repeated short pushes

Record:

- no-ballast push notes:
- 35 g push notes:
- 70 g push notes:

## Decision Gate

Do not redesign until these are answered:

- [ ] Is the real motor shaft height equal to the CAD assumption?
- [ ] Is the wheel opening correctly centered on the real axle?
- [ ] Is `70 g` ballast helpful or too much for the current drivetrain?
- [ ] Are the sensors at the right height?
- [ ] Is the skid material acceptable?
- [ ] Is any failure caused by geometry, not by weak TT hardware?

## Redesign Priority Rules

If motor fit is wrong:
- fix motor geometry first

If wheel clearance is wrong:
- fix axle datum and wheel window second

If battery or wiring shifts:
- fix retention before any shape changes

If push performance is poor but fit is correct:
- tune ballast and tires before changing the whole body

If performance is still poor after fit and ballast are correct:
- the next bottleneck is probably the drivetrain, not the chassis
