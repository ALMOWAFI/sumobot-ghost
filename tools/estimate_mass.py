from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
EXPORT_DIR = PROJECT_ROOT / "exports"
os.environ.setdefault("XDG_CACHE_HOME", str(PROJECT_ROOT / ".cache"))

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from sumobot_chassis import ChassisParams, build_ballast_insert, build_chassis, build_rear_skid
from build123d import CenterOf


PETG_DENSITY_G_PER_CM3 = 1.27
CHASSIS_PRINT_MATERIAL_FRACTION = (0.50, 0.60)
SKID_PRINT_MATERIAL_FRACTION = (0.90, 1.00)
MILD_STEEL_DENSITY_G_PER_CM3 = 7.85
LEAD_DENSITY_G_PER_CM3 = 11.34


@dataclass(frozen=True)
class MassRangeItem:
    name: str
    quantity: int
    unit_mass_g_low: float
    unit_mass_g_high: float
    basis: str
    note: str
    source: str | None = None

    @property
    def total_mass_g_low(self) -> float:
        return self.quantity * self.unit_mass_g_low

    @property
    def total_mass_g_high(self) -> float:
        return self.quantity * self.unit_mass_g_high

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["total_mass_g_low"] = round(self.total_mass_g_low, 2)
        data["total_mass_g_high"] = round(self.total_mass_g_high, 2)
        return data


def round_pair(values: tuple[float, float]) -> tuple[float, float]:
    return round(values[0], 2), round(values[1], 2)


def midpoint(low: float, high: float) -> float:
    return (low + high) / 2.0


def estimate_x_center_of_mass(
    *,
    params: ChassisParams,
    chassis_x_mm: float,
    chassis_mass_g: float,
    skid_mass_g: float,
    wheel_mass_g: float,
    battery_mass_g: float,
    switch_mass_g: float,
    wiring_mass_g: float,
    tb6612_mass_g: float,
    front_ballast_mass_g: float,
) -> float:
    half_length = params.chassis_length / 2
    weighted_items = [
        (chassis_mass_g, chassis_x_mm),
        (skid_mass_g, -half_length + 16.0),
        (2 * 30.6, params.motor_mount_x),
        (wheel_mass_g, params.motor_mount_x),
        (battery_mass_g, params.battery_x),
        (10.0, params.esp32_x),
        (11.23, params.buck_x),
        (switch_mass_g, -half_length + 3.0),
        (3.09, params.qtr_x),
        (0.5, params.vl53_x),
        (wiring_mass_g, -5.0),
        (tb6612_mass_g, -10.0),
        (front_ballast_mass_g, params.front_ballast_x),
    ]
    total_mass = sum(mass for mass, _ in weighted_items)
    return round(sum(mass * x for mass, x in weighted_items) / total_mass, 2)


def estimate_mass() -> dict[str, object]:
    params = ChassisParams()
    chassis = build_chassis(params)
    skid = build_rear_skid(params)
    ballast_insert = build_ballast_insert(params)
    bbox = chassis.bounding_box()
    chassis_com = chassis.center(CenterOf.MASS)

    chassis_volume_mm3 = float(chassis.volume)
    skid_volume_mm3 = float(skid.volume)
    ballast_insert_volume_mm3 = float(ballast_insert.volume)
    chassis_volume_cm3 = chassis_volume_mm3 / 1000.0
    skid_volume_cm3 = skid_volume_mm3 / 1000.0
    ballast_insert_volume_cm3 = ballast_insert_volume_mm3 / 1000.0

    chassis_solid_petg_mass_g = chassis_volume_cm3 * PETG_DENSITY_G_PER_CM3
    skid_solid_petg_mass_g = skid_volume_cm3 * PETG_DENSITY_G_PER_CM3
    ballast_insert_solid_petg_mass_g = ballast_insert_volume_cm3 * PETG_DENSITY_G_PER_CM3

    chassis_printed_petg_range_g = round_pair(
        (
            chassis_solid_petg_mass_g * CHASSIS_PRINT_MATERIAL_FRACTION[0],
            chassis_solid_petg_mass_g * CHASSIS_PRINT_MATERIAL_FRACTION[1],
        )
    )
    skid_printed_petg_range_g = round_pair(
        (
            skid_solid_petg_mass_g * SKID_PRINT_MATERIAL_FRACTION[0],
            skid_solid_petg_mass_g * SKID_PRINT_MATERIAL_FRACTION[1],
        )
    )
    ballast_insert_printed_petg_range_g = round_pair(
        (
            ballast_insert_solid_petg_mass_g * SKID_PRINT_MATERIAL_FRACTION[0],
            ballast_insert_solid_petg_mass_g * SKID_PRINT_MATERIAL_FRACTION[1],
        )
    )
    ballast_pair_volume_mm3 = (
        2
        * params.front_ballast_length
        * params.front_ballast_width
        * params.front_ballast_height
    )
    ballast_pair_volume_cm3 = ballast_pair_volume_mm3 / 1000.0
    ballast_pair_steel_capacity_g = round(ballast_pair_volume_cm3 * MILD_STEEL_DENSITY_G_PER_CM3, 2)
    ballast_pair_lead_capacity_g = round(ballast_pair_volume_cm3 * LEAD_DENSITY_G_PER_CM3, 2)
    standard_segment_total_count = params.front_ballast_segments_per_insert * 2
    standard_segment_total_mass_g = round(
        standard_segment_total_count * params.front_ballast_segment_mass, 2
    )

    required_items = [
        MassRangeItem(
            name="Printed chassis (PETG)",
            quantity=1,
            unit_mass_g_low=chassis_printed_petg_range_g[0],
            unit_mass_g_high=chassis_printed_petg_range_g[1],
            basis="CAD volume + material-density estimate",
            note="Uses actual CAD volume and an effective material fraction of 50% to 60% for a 35% infill, 4-5 wall functional print.",
            source="https://um-support-files.ultimaker.com/materials/2.85mm/sds/PETG/UM_PETG_KR_en_SDSv1.0.pdf",
        ),
        MassRangeItem(
            name="Rear skid wear part (PETG)",
            quantity=1,
            unit_mass_g_low=skid_printed_petg_range_g[0],
            unit_mass_g_high=skid_printed_petg_range_g[1],
            basis="CAD volume + material-density estimate",
            note="Thin skid prints almost solid in practice, so the effective material fraction is set to 90% to 100%.",
            source="https://um-support-files.ultimaker.com/materials/2.85mm/sds/PETG/UM_PETG_KR_en_SDSv1.0.pdf",
        ),
        MassRangeItem(
            name="TT DC gear motor",
            quantity=2,
            unit_mass_g_low=30.6,
            unit_mass_g_high=30.6,
            basis="vendor specification",
            note="SunFounder TT motor reference, 70 x 22 x 18 mm body.",
            source="https://docs.sunfounder.com/projects/3in1-kit-v2/en/latest/components/component_tt_motor.html",
        ),
        MassRangeItem(
            name="65 mm wheel",
            quantity=2,
            unit_mass_g_low=20.0,
            unit_mass_g_high=31.5,
            basis="vendor range",
            note="Mass varies across 65 mm TT/BO wheel variants, so the range captures lightweight 65 x 26 mm wheels up to heavier 65 mm TT wheels.",
            source="https://www.embeddinator.com/product/robot-wheel-65mm-for-dc-geared-motor | https://www.kiwi-electronics.com/en/thin-white-wheel-for-tt-motor-65mm-10319",
        ),
        MassRangeItem(
            name="7.4 V battery pack",
            quantity=1,
            unit_mass_g_low=87.0,
            unit_mass_g_high=100.0,
            basis="source-guided estimate",
            note="Lower bound follows a 7.4 V 1500 mAh pack at 87 g; upper bound is an engineering allowance for a slightly bulkier 70 x 40 x 20 mm pack.",
            source="https://myliontech.com/en/product/mylion-7-4v-1500mah-14500-lithium-ion-battery-pack/",
        ),
        MassRangeItem(
            name="ESP32 DevKit V1",
            quantity=1,
            unit_mass_g_low=10.0,
            unit_mass_g_high=10.0,
            basis="vendor specification",
            note="Grobotronics product listing.",
            source="https://grobotronics.com/esp32-development-board-devkit-v1.html?sl=en",
        ),
        MassRangeItem(
            name="LM2596 buck converter",
            quantity=1,
            unit_mass_g_low=11.23,
            unit_mass_g_high=11.23,
            basis="vendor specification",
            note="43.2 x 21 x 14 mm module reference.",
            source="https://www.microscale.net/products/lm2596-dc-dc-buck-converter",
        ),
        MassRangeItem(
            name="KCD1 rocker switch",
            quantity=1,
            unit_mass_g_low=4.0,
            unit_mass_g_high=6.0,
            basis="engineering estimate",
            note="Small KCD1-family panel switches typically land in the low single-digit gram range; use a scale once the exact switch is in hand.",
            source="https://abc-rc.pl/product-eng-16783-Przelacznik-kolyskowy-chwilowy-monostabilny-KCD1-21x15mm-ON-OFF-ON-250V-3PIN.html",
        ),
        MassRangeItem(
            name="QTR-8RC sensor array",
            quantity=1,
            unit_mass_g_low=3.09,
            unit_mass_g_high=3.09,
            basis="vendor specification",
            note="Pololu weight without headers.",
            source="https://www.pololu.com/product-info-merged/961",
        ),
        MassRangeItem(
            name="VL53L0X sensor",
            quantity=1,
            unit_mass_g_low=0.5,
            unit_mass_g_high=0.5,
            basis="vendor specification",
            note="Pololu weight without headers.",
            source="https://www.pololu.com/product/2490/specs",
        ),
        MassRangeItem(
            name="Fasteners, straps, hookup wire",
            quantity=1,
            unit_mass_g_low=18.0,
            unit_mass_g_high=30.0,
            basis="assembly allowance",
            note="Covers skid screws, zip ties or straps, sensor leads, power wiring, and short interconnects. Motor wire pigtails are already included in the motor mass.",
        ),
    ]

    optional_items = [
        MassRangeItem(
            name="Pair of ballast inserts (PETG)",
            quantity=2,
            unit_mass_g_low=ballast_insert_printed_petg_range_g[0],
            unit_mass_g_high=ballast_insert_printed_petg_range_g[1],
            basis="CAD volume + material-density estimate",
            note="One insert per bay, sized for five 1/4 oz steel segments each.",
            source="https://motionpro.com/product/08-0498",
        ),
        MassRangeItem(
            name="TB6612-class motor driver",
            quantity=1,
            unit_mass_g_low=1.5,
            unit_mass_g_high=3.0,
            basis="vendor range",
            note="Use this allowance only if you install a small TB6612-class carrier. A larger driver board changes both mass and packaging.",
            source="https://www.pololu.com/product/713/specs | https://www.robojunkies.com/products/tb6612fng-dual-channel-motor-driver-breakout",
        )
    ]
    ballast_insert_pair_item = optional_items[0]
    tb6612_item = optional_items[1]

    required_total_low = round(sum(item.total_mass_g_low for item in required_items), 2)
    required_total_high = round(sum(item.total_mass_g_high for item in required_items), 2)
    tb6612_total_low = round(required_total_low + tb6612_item.total_mass_g_low, 2)
    tb6612_total_high = round(required_total_high + tb6612_item.total_mass_g_high, 2)
    standard_ballast_total_low = round(
        tb6612_total_low + ballast_insert_pair_item.total_mass_g_low + standard_segment_total_mass_g,
        2,
    )
    standard_ballast_total_high = round(
        tb6612_total_high + ballast_insert_pair_item.total_mass_g_high + standard_segment_total_mass_g,
        2,
    )
    conservative_solid_plastic_high = round(
        tb6612_total_high
        - chassis_printed_petg_range_g[1]
        - skid_printed_petg_range_g[1]
        + chassis_solid_petg_mass_g
        + skid_solid_petg_mass_g,
        2,
    )
    chassis_mass_mid = midpoint(*chassis_printed_petg_range_g)
    skid_mass_mid = midpoint(*skid_printed_petg_range_g)
    wheel_mass_mid = midpoint(40.0, 63.0)
    battery_mass_mid = midpoint(87.0, 100.0)
    switch_mass_mid = midpoint(4.0, 6.0)
    wiring_mass_mid = midpoint(18.0, 30.0)
    tb6612_mass_mid = midpoint(1.5, 3.0)
    ballast_insert_pair_mass_mid = midpoint(
        2 * ballast_insert_printed_petg_range_g[0],
        2 * ballast_insert_printed_petg_range_g[1],
    )

    balance_scenarios = {
        "no_front_ballast_x_com_mm": estimate_x_center_of_mass(
            params=params,
            chassis_x_mm=float(chassis_com.X),
            chassis_mass_g=chassis_mass_mid,
            skid_mass_g=skid_mass_mid,
            wheel_mass_g=wheel_mass_mid,
            battery_mass_g=battery_mass_mid,
            switch_mass_g=switch_mass_mid,
            wiring_mass_g=wiring_mass_mid,
            tb6612_mass_g=tb6612_mass_mid + ballast_insert_pair_mass_mid,
            front_ballast_mass_g=0.0,
        ),
        "with_standard_insert_70g_ballast_x_com_mm": estimate_x_center_of_mass(
            params=params,
            chassis_x_mm=float(chassis_com.X),
            chassis_mass_g=chassis_mass_mid,
            skid_mass_g=skid_mass_mid,
            wheel_mass_g=wheel_mass_mid,
            battery_mass_g=battery_mass_mid,
            switch_mass_g=switch_mass_mid,
            wiring_mass_g=wiring_mass_mid,
            tb6612_mass_g=tb6612_mass_mid + ballast_insert_pair_mass_mid,
            front_ballast_mass_g=standard_segment_total_mass_g,
        ),
        "with_50g_front_ballast_x_com_mm": estimate_x_center_of_mass(
            params=params,
            chassis_x_mm=float(chassis_com.X),
            chassis_mass_g=chassis_mass_mid,
            skid_mass_g=skid_mass_mid,
            wheel_mass_g=wheel_mass_mid,
            battery_mass_g=battery_mass_mid,
            switch_mass_g=switch_mass_mid,
            wiring_mass_g=wiring_mass_mid,
            tb6612_mass_g=tb6612_mass_mid + ballast_insert_pair_mass_mid,
            front_ballast_mass_g=50.0,
        ),
        "with_100g_front_ballast_x_com_mm": estimate_x_center_of_mass(
            params=params,
            chassis_x_mm=float(chassis_com.X),
            chassis_mass_g=chassis_mass_mid,
            skid_mass_g=skid_mass_mid,
            wheel_mass_g=wheel_mass_mid,
            battery_mass_g=battery_mass_mid,
            switch_mass_g=switch_mass_mid,
            wiring_mass_g=wiring_mass_mid,
            tb6612_mass_g=tb6612_mass_mid + ballast_insert_pair_mass_mid,
            front_ballast_mass_g=100.0,
        ),
        "with_150g_front_ballast_x_com_mm": estimate_x_center_of_mass(
            params=params,
            chassis_x_mm=float(chassis_com.X),
            chassis_mass_g=chassis_mass_mid,
            skid_mass_g=skid_mass_mid,
            wheel_mass_g=wheel_mass_mid,
            battery_mass_g=battery_mass_mid,
            switch_mass_g=switch_mass_mid,
            wiring_mass_g=wiring_mass_mid,
            tb6612_mass_g=tb6612_mass_mid + ballast_insert_pair_mass_mid,
            front_ballast_mass_g=150.0,
        ),
    }

    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "legal_mass_limit_g": 1000.0,
        "cad_metrics": {
            "outer_envelope_mm": {
                "length": round(float(bbox.max.X - bbox.min.X), 3),
                "width": round(float(bbox.max.Y - bbox.min.Y), 3),
                "height": round(float(bbox.max.Z - bbox.min.Z), 3),
            },
            "chassis_x_center_of_mass_mm": round(float(chassis_com.X), 3),
            "chassis_volume_mm3": round(chassis_volume_mm3, 3),
            "rear_skid_volume_mm3": round(skid_volume_mm3, 3),
            "ballast_insert_volume_mm3": round(ballast_insert_volume_mm3, 3),
            "chassis_solid_petg_mass_g": round(chassis_solid_petg_mass_g, 2),
            "rear_skid_solid_petg_mass_g": round(skid_solid_petg_mass_g, 2),
            "ballast_insert_solid_petg_mass_g": round(ballast_insert_solid_petg_mass_g, 2),
            "printed_chassis_mass_g_range": {
                "low": chassis_printed_petg_range_g[0],
                "high": chassis_printed_petg_range_g[1],
            },
            "printed_rear_skid_mass_g_range": {
                "low": skid_printed_petg_range_g[0],
                "high": skid_printed_petg_range_g[1],
            },
            "printed_ballast_insert_mass_g_range": {
                "low": ballast_insert_printed_petg_range_g[0],
                "high": ballast_insert_printed_petg_range_g[1],
            },
            "front_ballast_pair_internal_volume_mm3": round(ballast_pair_volume_mm3, 3),
            "front_ballast_pair_capacity_g": {
                "mild_steel_full_fill": ballast_pair_steel_capacity_g,
                "lead_full_fill": ballast_pair_lead_capacity_g,
                "standard_1_4oz_segment_total": standard_segment_total_mass_g,
            },
            "front_ballast_standard_segment_count_total": standard_segment_total_count,
        },
        "required_items": [item.to_dict() for item in required_items],
        "optional_items": [item.to_dict() for item in optional_items],
        "balance_scenarios": balance_scenarios,
        "totals_g": {
            "required_assembled_low": required_total_low,
            "required_assembled_high": required_total_high,
            "with_ballast_insert_pair_and_tb6612_low": round(
                tb6612_total_low + ballast_insert_pair_item.total_mass_g_low, 2
            ),
            "with_ballast_insert_pair_and_tb6612_high": round(
                tb6612_total_high + ballast_insert_pair_item.total_mass_g_high, 2
            ),
            "with_tb6612_class_driver_low": tb6612_total_low,
            "with_tb6612_class_driver_high": tb6612_total_high,
            "with_standard_inserted_70g_ballast_low": standard_ballast_total_low,
            "with_standard_inserted_70g_ballast_high": standard_ballast_total_high,
            "conservative_solid_plastic_with_tb6612_high": conservative_solid_plastic_high,
            "mass_margin_to_1kg_with_tb6612_low": round(1000.0 - tb6612_total_high, 2),
            "mass_margin_to_1kg_with_tb6612_high": round(1000.0 - tb6612_total_low, 2),
        },
        "open_items": [
            "The exact battery chemistry and capacity are still unspecified, so the battery remains the largest single mass uncertainty.",
            "Wheel mass varies a lot between 65 mm variants, so the wheel pair is modeled as a range instead of a fixed value.",
            "The current parts list still does not lock the motor-driver board; the optional TB6612-class allowance assumes a small breakout, not a heavy L298N-style board.",
            "Front ballast capacity is a geometric maximum; the practical ballast mass depends on the slug shape and the chosen ballast material.",
            "The standard wheel-weight insert is based on a 1/4 oz steel segment form factor; the segment thickness is an engineering inference from listed mass, face dimensions, and steel density.",
        ],
        "sources": [
            "https://docs.sunfounder.com/projects/3in1-kit-v2/en/latest/components/component_tt_motor.html",
            "https://www.pololu.com/product-info-merged/961",
            "https://www.pololu.com/product/2490/specs",
            "https://grobotronics.com/esp32-development-board-devkit-v1.html?sl=en",
            "https://www.microscale.net/products/lm2596-dc-dc-buck-converter",
            "https://www.embeddinator.com/product/robot-wheel-65mm-for-dc-geared-motor",
            "https://www.kiwi-electronics.com/en/thin-white-wheel-for-tt-motor-65mm-10319",
            "https://myliontech.com/en/product/mylion-7-4v-1500mah-14500-lithium-ion-battery-pack/",
            "https://motionpro.com/product/08-0498",
            "https://www.pololu.com/product/713/specs",
            "https://um-support-files.ultimaker.com/materials/2.85mm/sds/PETG/UM_PETG_KR_en_SDSv1.0.pdf",
        ],
    }
    return report


def report_markdown(report: dict[str, object]) -> str:
    totals = report["totals_g"]
    cad_metrics = report["cad_metrics"]
    balance = report["balance_scenarios"]
    lines = [
        "# Sumo Bot Mass Estimate",
        "",
        "## Summary",
        "",
        f"- Required assembled mass range: {totals['required_assembled_low']} to {totals['required_assembled_high']} g",
        f"- With small TB6612-class motor driver: {totals['with_tb6612_class_driver_low']} to {totals['with_tb6612_class_driver_high']} g",
        f"- With ballast inserts, TB6612-class driver, and ten standard 1/4 oz steel segments: {totals['with_standard_inserted_70g_ballast_low']} to {totals['with_standard_inserted_70g_ballast_high']} g",
        f"- Conservative solid-plastic upper bound with TB6612-class driver: {totals['conservative_solid_plastic_with_tb6612_high']} g",
        f"- Margin to 1 kg limit with TB6612-class driver: {totals['mass_margin_to_1kg_with_tb6612_low']} to {totals['mass_margin_to_1kg_with_tb6612_high']} g",
        "",
        "## CAD-Derived Plastic Mass",
        "",
        f"- Chassis CAD volume: {cad_metrics['chassis_volume_mm3']} mm^3",
        f"- Rear skid CAD volume: {cad_metrics['rear_skid_volume_mm3']} mm^3",
        f"- Ballast insert CAD volume: {cad_metrics['ballast_insert_volume_mm3']} mm^3 per insert",
        f"- Chassis solid PETG equivalent: {cad_metrics['chassis_solid_petg_mass_g']} g",
        f"- Rear skid solid PETG equivalent: {cad_metrics['rear_skid_solid_petg_mass_g']} g",
        f"- Ballast insert solid PETG equivalent: {cad_metrics['ballast_insert_solid_petg_mass_g']} g per insert",
        f"- Printed chassis estimate: {cad_metrics['printed_chassis_mass_g_range']['low']} to {cad_metrics['printed_chassis_mass_g_range']['high']} g",
        f"- Printed rear skid estimate: {cad_metrics['printed_rear_skid_mass_g_range']['low']} to {cad_metrics['printed_rear_skid_mass_g_range']['high']} g",
        f"- Printed ballast insert estimate: {cad_metrics['printed_ballast_insert_mass_g_range']['low']} to {cad_metrics['printed_ballast_insert_mass_g_range']['high']} g per insert",
        f"- Chassis x-center of mass from CAD alone: {cad_metrics['chassis_x_center_of_mass_mm']} mm",
        f"- Front ballast pair internal volume: {cad_metrics['front_ballast_pair_internal_volume_mm3']} mm^3",
        f"- Front ballast pair capacity if fully filled: {cad_metrics['front_ballast_pair_capacity_g']['mild_steel_full_fill']} g steel or {cad_metrics['front_ballast_pair_capacity_g']['lead_full_fill']} g lead",
        f"- Standard insert capacity: {cad_metrics['front_ballast_standard_segment_count_total']} total 1/4 oz steel segments, or {cad_metrics['front_ballast_pair_capacity_g']['standard_1_4oz_segment_total']} g",
        "",
        "## Estimated X-Balance",
        "",
        f"- No front ballast: x COM {balance['no_front_ballast_x_com_mm']} mm",
        f"- With standard insert loaded to 70 g: x COM {balance['with_standard_insert_70g_ballast_x_com_mm']} mm",
        f"- With 50 g front ballast: x COM {balance['with_50g_front_ballast_x_com_mm']} mm",
        f"- With 100 g front ballast: x COM {balance['with_100g_front_ballast_x_com_mm']} mm",
        f"- With 150 g front ballast: x COM {balance['with_150g_front_ballast_x_com_mm']} mm",
        "",
        "## Required Items",
        "",
    ]

    for item in report["required_items"]:
        item_range = f"{item['total_mass_g_low']} to {item['total_mass_g_high']} g"
        lines.append(f"- {item['name']}: {item_range}. {item['note']}")

    lines.extend(
        [
            "",
            "## Optional Item",
            "",
        ]
    )

    for item in report["optional_items"]:
        item_range = f"{item['total_mass_g_low']} to {item['total_mass_g_high']} g"
        lines.append(f"- {item['name']}: {item_range}. {item['note']}")

    lines.extend(
        [
            "",
            "## Open Items",
            "",
        ]
    )
    lines.extend(f"- {entry}" for entry in report["open_items"])
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    report = estimate_mass()
    json_path = EXPORT_DIR / "sumobot_mass_estimate.json"
    md_path = EXPORT_DIR / "sumobot_mass_estimate.md"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    md_path.write_text(report_markdown(report), encoding="utf-8")

    totals = report["totals_g"]
    print(f"Required assembled mass: {totals['required_assembled_low']} g to {totals['required_assembled_high']} g")
    print(
        "With TB6612-class driver: "
        f"{totals['with_tb6612_class_driver_low']} g to {totals['with_tb6612_class_driver_high']} g"
    )
    print(f"Mass report JSON: {json_path}")
    print(f"Mass report Markdown: {md_path}")


if __name__ == "__main__":
    main()
