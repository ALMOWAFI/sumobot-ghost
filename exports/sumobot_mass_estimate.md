# Sumo Bot Mass Estimate

## Summary

- Required assembled mass range: 377.68 to 456.06 g
- With small TB6612-class motor driver: 379.18 to 459.06 g
- With ballast inserts, TB6612-class driver, and ten standard 1/4 oz steel segments: 452.94 to 533.24 g
- Conservative solid-plastic upper bound with TB6612-class driver: 571.84 g
- Margin to 1 kg limit with TB6612-class driver: 540.94 to 620.82 g

## CAD-Derived Plastic Mass

- Chassis CAD volume: 222003.83 mm^3
- Rear skid CAD volume: 1476.0 mm^3
- Ballast insert CAD volume: 1646.048 mm^3 per insert
- Chassis solid PETG equivalent: 281.94 g
- Rear skid solid PETG equivalent: 1.87 g
- Ballast insert solid PETG equivalent: 2.09 g per insert
- Printed chassis estimate: 140.97 to 169.17 g
- Printed rear skid estimate: 1.69 to 1.87 g
- Printed ballast insert estimate: 1.88 to 2.09 g per insert
- Chassis x-center of mass from CAD alone: 5.857 mm
- Front ballast pair internal volume: 15288.0 mm^3
- Front ballast pair capacity if fully filled: 120.01 g steel or 173.37 g lead
- Standard insert capacity: 10 total 1/4 oz steel segments, or 70.0 g

## Estimated X-Balance

- No front ballast: x COM -0.91 mm
- With standard insert loaded to 70 g: x COM 5.6 mm
- With 50 g front ballast: x COM 3.94 mm
- With 100 g front ballast: x COM 7.86 mm
- With 150 g front ballast: x COM 11.1 mm

## Required Items

- Printed chassis (PETG): 140.97 to 169.17 g. Uses actual CAD volume and an effective material fraction of 50% to 60% for a 35% infill, 4-5 wall functional print.
- Rear skid wear part (PETG): 1.69 to 1.87 g. Thin skid prints almost solid in practice, so the effective material fraction is set to 90% to 100%.
- TT DC gear motor: 61.2 to 61.2 g. SunFounder TT motor reference, 70 x 22 x 18 mm body.
- 65 mm wheel: 40.0 to 63.0 g. Mass varies across 65 mm TT/BO wheel variants, so the range captures lightweight 65 x 26 mm wheels up to heavier 65 mm TT wheels.
- 7.4 V battery pack: 87.0 to 100.0 g. Lower bound follows a 7.4 V 1500 mAh pack at 87 g; upper bound is an engineering allowance for a slightly bulkier 70 x 40 x 20 mm pack.
- ESP32 DevKit V1: 10.0 to 10.0 g. Grobotronics product listing.
- LM2596 buck converter: 11.23 to 11.23 g. 43.2 x 21 x 14 mm module reference.
- KCD1 rocker switch: 4.0 to 6.0 g. Small KCD1-family panel switches typically land in the low single-digit gram range; use a scale once the exact switch is in hand.
- QTR-8RC sensor array: 3.09 to 3.09 g. Pololu weight without headers.
- VL53L0X sensor: 0.5 to 0.5 g. Pololu weight without headers.
- Fasteners, straps, hookup wire: 18.0 to 30.0 g. Covers skid screws, zip ties or straps, sensor leads, power wiring, and short interconnects. Motor wire pigtails are already included in the motor mass.

## Optional Item

- Pair of ballast inserts (PETG): 3.76 to 4.18 g. One insert per bay, sized for five 1/4 oz steel segments each.
- TB6612-class motor driver: 1.5 to 3.0 g. Use this allowance only if you install a small TB6612-class carrier. A larger driver board changes both mass and packaging.

## Open Items

- The exact battery chemistry and capacity are still unspecified, so the battery remains the largest single mass uncertainty.
- Wheel mass varies a lot between 65 mm variants, so the wheel pair is modeled as a range instead of a fixed value.
- The current parts list still does not lock the motor-driver board; the optional TB6612-class allowance assumes a small breakout, not a heavy L298N-style board.
- Front ballast capacity is a geometric maximum; the practical ballast mass depends on the slug shape and the chosen ballast material.
- The standard wheel-weight insert is based on a 1/4 oz steel segment form factor; the segment thickness is an engineering inference from listed mass, face dimensions, and steel density.
