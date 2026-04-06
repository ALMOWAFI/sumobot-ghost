from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.environ.setdefault("XDG_CACHE_HOME", str(PROJECT_ROOT / ".cache"))

from build123d import Align, Box, Cylinder, Pos, chamfer
from build123d.exporters3d import export_step, export_stl

EXPORT_DIR = PROJECT_ROOT / "exports"


@dataclass(frozen=True)
class ChassisParams:
    chassis_length: float = 182.0
    chassis_width: float = 168.0
    base_thickness: float = 4.0
    wall_thickness: float = 3.0
    wall_height: float = 28.0

    wedge_length: float = 62.0
    wedge_width: float = 160.0
    wedge_height: float = 16.0
    wedge_back_flat: float = 8.0
    wedge_nose_height: float = 0.5

    motor_mount_x: float = -18.0
    motor_length: float = 70.0
    motor_width: float = 23.0
    motor_height: float = 18.0
    motor_clearance: float = 1.0
    motor_guide_thickness: float = 3.0
    motor_stop_thickness: float = 3.0
    motor_retainer_height: float = 14.0
    motor_shaft_center_from_floor: float = 10.5
    motor_strap_slot_width: float = 4.0
    motor_strap_slot_depth: float = 18.0
    wheel_window_length: float = 58.0
    wheel_window_height: float = 36.0
    wheel_window_width: float = 6.0

    battery_x: float = 18.0
    battery_length: float = 70.0
    battery_width: float = 40.0
    battery_height: float = 20.0
    battery_clearance: float = 1.5
    battery_rail_height: float = 14.0
    battery_rail_thickness: float = 3.0
    battery_strap_slot_length: float = 16.0
    battery_strap_slot_width: float = 4.0
    battery_lead_notch_length: float = 12.0
    battery_lead_notch_height: float = 8.0
    battery_side_relief_length: float = 20.0
    battery_side_relief_width: float = 12.0
    battery_side_relief_height: float = 10.0

    esp32_x: float = -22.0
    esp32_y: float = 27.0
    esp32_length: float = 55.0
    esp32_width: float = 28.0
    esp32_height: float = 15.0
    esp32_rail_height: float = 8.0
    esp32_end_tab_thickness: float = 3.0
    esp32_end_tab_width: float = 8.0
    esp32_end_tab_height: float = 6.0

    buck_x: float = -22.0
    buck_y: float = -25.0
    buck_length: float = 45.0
    buck_width: float = 22.0
    buck_height: float = 15.0
    buck_rail_height: float = 8.0

    board_rail_thickness: float = 2.5
    board_strap_slot_length: float = 12.0
    board_strap_slot_width: float = 4.0
    buck_mount_slot_span_x: float = 34.0
    buck_mount_slot_span_y: float = 14.0
    buck_mount_slot_length: float = 8.0
    buck_mount_slot_width: float = 3.2

    rear_bridge_length: float = 22.0
    rear_bridge_width: float = 36.0
    rear_bridge_height: float = 10.0
    skid_hole_spacing: float = 24.0
    skid_hole_diameter: float = 3.2
    skid_part_length: float = 34.0
    skid_part_width: float = 18.0
    skid_part_thickness: float = 2.5
    skid_slot_length: float = 6.0
    skid_slot_width: float = 3.4

    switch_slot_width: float = 19.0
    switch_slot_height: float = 13.0
    switch_slot_z: float = 16.0
    switch_guard_depth: float = 6.0
    switch_guard_width: float = 6.0
    switch_guard_height: float = 14.0
    switch_guard_gap: float = 24.0
    switch_guard_roof_width: float = 32.0
    switch_guard_roof_thickness: float = 3.0

    qtr_x: float = 77.0
    qtr_length: float = 75.0
    qtr_width: float = 13.0
    qtr_mount_depth: float = 18.0
    qtr_mount_height: float = 5.0
    qtr_slot_spacing: float = 62.0
    qtr_slot_length: float = 6.0
    qtr_slot_width: float = 2.4

    vl53_x: float = 72.0
    vl53_y: float = 0.0
    vl53_length: float = 25.0
    vl53_width: float = 13.0
    vl53_mount_depth: float = 17.0
    vl53_mount_height: float = 8.0
    vl53_slot_spacing: float = 12.0
    vl53_slot_length: float = 4.0
    vl53_slot_width: float = 2.2

    front_ballast_x: float = 45.0
    front_ballast_y: float = 56.0
    front_ballast_length: float = 26.0
    front_ballast_width: float = 21.0
    front_ballast_height: float = 14.0
    front_ballast_rail_thickness: float = 3.0
    front_ballast_strap_slot_length: float = 12.0
    front_ballast_strap_slot_width: float = 4.0
    front_ballast_segment_length: float = 20.4
    front_ballast_segment_face_width: float = 13.1
    front_ballast_segment_mass: float = 7.0
    front_ballast_segment_thickness_assumed: float = 3.35
    front_ballast_segments_per_insert: int = 5
    front_ballast_insert_clearance: float = 0.3
    front_ballast_insert_floor_thickness: float = 0.6
    front_ballast_insert_wall_thickness: float = 0.6
    front_ballast_insert_divider_thickness: float = 0.5
    front_ballast_insert_top_clearance: float = 0.3

    rear_corner_cut_size: float = 26.0
    floor_recess_depth: float = 1.2
    floor_recess_length: float = 74.0
    floor_recess_width: float = 44.0

    wire_trench_depth: float = 1.4
    wire_trench_width: float = 6.0
    wire_anchor_slot_length: float = 7.0
    wire_anchor_slot_width: float = 2.5
    motor_wire_pass_length: float = 10.0
    motor_wire_pass_height: float = 8.0
    board_wire_pass_length: float = 10.0
    board_wire_pass_width: float = 6.0
    board_wire_pass_height: float = 8.0
    board_service_relief_length: float = 20.0
    board_service_relief_width: float = 12.0
    board_service_relief_height: float = 10.0
    esp32_usb_opening_length: float = 20.0
    esp32_usb_opening_width: float = 14.0
    esp32_usb_opening_height: float = 12.0
    esp32_usb_relief_depth: float = 16.0
    esp32_usb_relief_width: float = 18.0
    esp32_usb_relief_height: float = 12.0
    sensor_wire_slot_width: float = 5.0
    sensor_wire_slot_height: float = 6.0

    wheel_diameter_assumption: float = 65.0
    wheel_width_assumption: float = 26.0


def box_min(length: float, width: float, height: float, x: float, y: float, z: float):
    return Pos(x, y, z) * Box(
        length,
        width,
        height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )


def box_center(length: float, width: float, height: float, x: float, y: float, z: float):
    return Pos(x, y, z) * Box(
        length,
        width,
        height,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    )


def cylinder_min(radius: float, height: float, x: float, y: float, z: float):
    return Pos(x, y, z) * Cylinder(radius, height, align=(Align.CENTER, Align.CENTER, Align.MIN))


def tray_rails(
    *,
    center_x: float,
    center_y: float,
    inner_length: float,
    inner_width: float,
    rail_thickness: float,
    rail_height: float,
    floor_z: float,
):
    outer_length = inner_length + 2 * rail_thickness
    outer_width = inner_width + 2 * rail_thickness
    half_inner_x = inner_length / 2 + rail_thickness / 2
    half_inner_y = inner_width / 2 + rail_thickness / 2

    return (
        box_min(outer_length, rail_thickness, rail_height, center_x, center_y + half_inner_y, floor_z)
        + box_min(outer_length, rail_thickness, rail_height, center_x, center_y - half_inner_y, floor_z)
        + box_min(rail_thickness, outer_width, rail_height, center_x + half_inner_x, center_y, floor_z)
        + box_min(rail_thickness, outer_width, rail_height, center_x - half_inner_x, center_y, floor_z)
    )


def build_chassis(params: ChassisParams):
    floor_top_z = params.base_thickness
    half_length = params.chassis_length / 2
    half_width = params.chassis_width / 2
    wedge_center_x = half_length - params.wedge_length / 2
    side_wall_length = params.chassis_length - params.wedge_length
    side_wall_center_x = -params.wedge_length / 2
    rear_wall_x = -half_length + params.wall_thickness / 2
    left_wall_y = half_width - params.wall_thickness / 2
    right_wall_y = -left_wall_y

    motor_pocket_width = (
        params.motor_width + 2 * params.motor_clearance + params.motor_guide_thickness
    )
    motor_y = half_width - params.wall_thickness - params.motor_width / 2
    motor_pocket_center_y = half_width - params.wall_thickness - motor_pocket_width / 2
    inner_guide_y = half_width - params.wall_thickness - motor_pocket_width + params.motor_guide_thickness / 2
    motor_axle_z = floor_top_z + params.motor_shaft_center_from_floor
    front_sensor_wire_x = params.qtr_x - params.qtr_mount_depth / 2 - 9.0
    battery_rail_center_y = (
        params.battery_width / 2 + params.battery_clearance + params.battery_rail_thickness / 2
    )
    esp32_inner_rail_y = params.esp32_y - (
        params.esp32_width / 2 + params.board_rail_thickness / 2
    )
    buck_inner_rail_y = params.buck_y + (
        params.buck_width / 2 + params.board_rail_thickness / 2
    )

    chassis = box_min(
        params.chassis_length,
        params.chassis_width,
        params.base_thickness,
        0,
        0,
        0,
    )
    chassis += box_min(
        side_wall_length,
        params.wall_thickness,
        params.wall_height,
        side_wall_center_x,
        left_wall_y,
        floor_top_z,
    )
    chassis += box_min(
        side_wall_length,
        params.wall_thickness,
        params.wall_height,
        side_wall_center_x,
        right_wall_y,
        floor_top_z,
    )
    chassis += box_min(
        params.wall_thickness,
        params.chassis_width,
        params.wall_height,
        rear_wall_x,
        0,
        floor_top_z,
    )

    wedge_block = box_min(
        params.wedge_length,
        params.wedge_width,
        params.wedge_height,
        wedge_center_x,
        0,
        0,
    )
    wedge_front_x = half_length
    wedge_top_z = params.wedge_height
    target_edges = [
        edge
        for edge in wedge_block.edges()
        if abs(edge.center().X - wedge_front_x) < 0.001
        and abs(edge.center().Z - wedge_top_z) < 0.001
    ]
    wedge = chamfer(
        target_edges,
        params.wedge_height - params.wedge_nose_height,
        params.wedge_length - params.wedge_back_flat,
    )
    chassis += wedge

    for direction in (1, -1):
        chassis += box_min(
            params.motor_length + 2 * params.motor_clearance,
            params.motor_guide_thickness,
            params.motor_retainer_height,
            params.motor_mount_x,
            direction * inner_guide_y,
            floor_top_z,
        )
        for stop_x in (
            params.motor_mount_x
            - (params.motor_length / 2 + params.motor_clearance + params.motor_stop_thickness / 2),
            params.motor_mount_x
            + (params.motor_length / 2 + params.motor_clearance + params.motor_stop_thickness / 2),
        ):
            chassis += box_min(
                params.motor_stop_thickness,
                motor_pocket_width,
                params.motor_retainer_height,
                stop_x,
                direction * motor_pocket_center_y,
                floor_top_z,
            )

    chassis += tray_rails(
        center_x=params.battery_x,
        center_y=0,
        inner_length=params.battery_length + 2 * params.battery_clearance,
        inner_width=params.battery_width + 2 * params.battery_clearance,
        rail_thickness=params.battery_rail_thickness,
        rail_height=params.battery_rail_height,
        floor_z=floor_top_z,
    )
    chassis += tray_rails(
        center_x=params.esp32_x,
        center_y=params.esp32_y,
        inner_length=params.esp32_length,
        inner_width=params.esp32_width,
        rail_thickness=params.board_rail_thickness,
        rail_height=params.esp32_rail_height,
        floor_z=floor_top_z,
    )
    chassis += box_min(
        params.esp32_end_tab_thickness,
        params.esp32_end_tab_width,
        params.esp32_end_tab_height,
        params.esp32_x - params.esp32_length / 2 - params.board_rail_thickness / 2,
        params.esp32_y,
        floor_top_z,
    )
    for tab_y in (
        params.esp32_y - params.esp32_usb_relief_width / 2,
        params.esp32_y + params.esp32_usb_relief_width / 2,
    ):
        chassis += box_min(
            params.esp32_end_tab_thickness,
            params.esp32_end_tab_width,
            params.esp32_end_tab_height,
            params.esp32_x + params.esp32_length / 2 + params.board_rail_thickness / 2,
            tab_y,
            floor_top_z,
        )
    chassis += tray_rails(
        center_x=params.buck_x,
        center_y=params.buck_y,
        inner_length=params.buck_length,
        inner_width=params.buck_width,
        rail_thickness=params.board_rail_thickness,
        rail_height=params.buck_rail_height,
        floor_z=floor_top_z,
    )
    chassis += box_min(
        params.rear_bridge_length,
        params.rear_bridge_width,
        params.rear_bridge_height,
        -half_length + 16.0,
        0,
        floor_top_z,
    )
    chassis += box_min(
        params.qtr_mount_depth,
        params.qtr_length + 6.0,
        params.qtr_mount_height,
        params.qtr_x,
        0,
        floor_top_z,
    )
    chassis += box_min(
        params.vl53_length + 6.0,
        params.vl53_mount_depth,
        params.vl53_mount_height,
        params.vl53_x,
        params.vl53_y,
        floor_top_z,
    )
    for direction in (1, -1):
        chassis += tray_rails(
            center_x=params.front_ballast_x,
            center_y=direction * params.front_ballast_y,
            inner_length=params.front_ballast_length,
            inner_width=params.front_ballast_width,
            rail_thickness=params.front_ballast_rail_thickness,
            rail_height=params.front_ballast_height,
            floor_z=floor_top_z,
        )
    rear_guard_x = -half_length - params.switch_guard_depth / 2
    for guard_y in (
        -params.switch_guard_gap / 2,
        params.switch_guard_gap / 2,
    ):
        chassis += box_min(
            params.switch_guard_depth,
            params.switch_guard_width,
            params.switch_guard_height,
            rear_guard_x,
            guard_y,
            floor_top_z + params.switch_slot_z - params.switch_guard_height / 2,
        )
    chassis += box_min(
        params.switch_guard_depth,
        params.switch_guard_roof_width,
        params.switch_guard_roof_thickness,
        rear_guard_x,
        0,
        floor_top_z + params.switch_slot_z + params.switch_slot_height / 2 + 2.0,
    )

    cutouts = None

    def add_cutout(shape):
        nonlocal cutouts
        cutouts = shape if cutouts is None else cutouts + shape

    for direction in (1, -1):
        side_y = direction * motor_y
        strap_offsets = (-18.0, 18.0)
        for offset in strap_offsets:
            add_cutout(
                box_center(
                    params.motor_strap_slot_width,
                    params.motor_strap_slot_depth,
                    params.motor_retainer_height + params.base_thickness + 1.0,
                    params.motor_mount_x + offset,
                    side_y,
                    (params.motor_retainer_height + params.base_thickness) / 2,
                )
            )
        add_cutout(
            box_center(
                params.wheel_window_length,
                params.wheel_window_width,
                params.wheel_window_height,
                params.motor_mount_x,
                direction * (half_width - params.wall_thickness / 2),
                motor_axle_z,
            )
        )
        add_cutout(
            box_center(
                params.motor_wire_pass_length,
                params.wall_thickness + 2.0,
                params.motor_wire_pass_height,
                params.motor_mount_x - params.motor_length / 2 + 8.0,
                direction * (half_width - params.wall_thickness / 2),
                floor_top_z + params.motor_wire_pass_height / 2,
            )
        )

    corner_cut_center_x = -half_length + params.rear_corner_cut_size / 2 - 2.0
    corner_cut_z = floor_top_z + (params.wall_height + 1.0) / 2
    for direction in (1, -1):
        corner_cut = Pos(
            corner_cut_center_x,
            direction * (half_width - params.rear_corner_cut_size / 2 + 2.0),
            corner_cut_z,
        ) * Box(
            params.rear_corner_cut_size,
            params.rear_corner_cut_size,
            params.wall_height + 1.0,
            rotation=(0, 0, 45),
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        )
        add_cutout(corner_cut)

    # Shallow trenches keep wiring low and predictable instead of floating above the floor.
    add_cutout(
        box_min(
            params.chassis_length - params.wedge_length - 22.0,
            params.wire_trench_width,
            params.wire_trench_depth,
            -10.0,
            0,
            params.base_thickness - params.wire_trench_depth,
        )
    )
    add_cutout(
        box_min(
            44.0,
            params.wire_trench_width,
            params.wire_trench_depth,
            38.0,
            0,
            params.base_thickness - params.wire_trench_depth,
        )
    )
    add_cutout(
        box_min(
            26.0,
            44.0,
            params.wire_trench_depth,
            params.esp32_x + 6.0,
            18.0,
            params.base_thickness - params.wire_trench_depth,
        )
    )
    add_cutout(
        box_min(
            26.0,
            40.0,
            params.wire_trench_depth,
            params.buck_x + 6.0,
            -17.0,
            params.base_thickness - params.wire_trench_depth,
        )
    )
    for direction in (1, -1):
        add_cutout(
            box_min(
                24.0,
                14.0,
                params.wire_trench_depth,
                params.motor_mount_x - 22.0,
                direction * 43.0,
                params.base_thickness - params.wire_trench_depth,
            )
        )

    add_cutout(
        box_min(
            params.floor_recess_length,
            params.floor_recess_width,
            params.floor_recess_depth,
            params.battery_x,
            0,
            params.base_thickness - params.floor_recess_depth,
        )
    )
    add_cutout(
        box_center(
            params.battery_lead_notch_length,
            params.battery_rail_thickness + 2.0,
            params.battery_lead_notch_height,
            params.battery_x - params.battery_length / 2 + 10.0,
            -battery_rail_center_y,
            floor_top_z + params.battery_lead_notch_height / 2,
        )
    )
    for direction in (1, -1):
        add_cutout(
            box_center(
                params.battery_side_relief_length,
                params.battery_side_relief_width,
                params.battery_side_relief_height,
                params.battery_x,
                direction * battery_rail_center_y,
                floor_top_z + params.battery_side_relief_height / 2,
            )
        )
    add_cutout(
        box_min(
            18.0,
            params.wire_trench_width,
            params.wire_trench_depth,
            params.battery_x - params.battery_length / 2 + 6.0,
            -14.0,
            params.base_thickness - params.wire_trench_depth,
        )
    )

    battery_slot_y = params.battery_width / 2 + params.battery_clearance / 2 + 4.0
    for slot_x in (
        params.battery_x - params.battery_length / 4,
        params.battery_x + params.battery_length / 4,
    ):
        for slot_y in (-battery_slot_y, battery_slot_y):
            add_cutout(
                box_center(
                    params.battery_strap_slot_length,
                    params.battery_strap_slot_width,
                    params.base_thickness + 1.0,
                    slot_x,
                    slot_y,
                    params.base_thickness / 2,
                )
            )

    for center_x, center_y, span_x, span_y in (
        (params.esp32_x, params.esp32_y, params.esp32_length / 4, params.esp32_width / 2 + 3.0),
        (params.buck_x, params.buck_y, params.buck_length / 4, params.buck_width / 2 + 3.0),
    ):
        for slot_x in (center_x - span_x, center_x + span_x):
            for slot_y in (center_y - span_y, center_y + span_y):
                add_cutout(
                    box_center(
                        params.board_strap_slot_length,
                        params.board_strap_slot_width,
                        params.base_thickness + 1.0,
                        slot_x,
                        slot_y,
                        params.base_thickness / 2,
                    )
                )

    add_cutout(
        box_center(
            params.board_wire_pass_length,
            params.board_wire_pass_width,
            params.board_wire_pass_height,
            params.esp32_x + params.esp32_length / 2 + params.board_rail_thickness,
            params.esp32_y,
            floor_top_z + params.board_wire_pass_height / 2,
        )
    )
    add_cutout(
        box_center(
            params.board_wire_pass_length,
            params.board_wire_pass_width,
            params.board_wire_pass_height,
            params.buck_x + params.buck_length / 2 + params.board_rail_thickness,
            params.buck_y,
            floor_top_z + params.board_wire_pass_height / 2,
        )
    )
    add_cutout(
        box_center(
            params.board_service_relief_length,
            params.board_service_relief_width,
            params.board_service_relief_height,
            params.esp32_x,
            esp32_inner_rail_y,
            floor_top_z + params.board_service_relief_height / 2,
        )
    )
    add_cutout(
        box_center(
            params.board_service_relief_length,
            params.board_service_relief_width,
            params.board_service_relief_height,
            params.buck_x,
            buck_inner_rail_y,
            floor_top_z + params.board_service_relief_height / 2,
        )
    )
    add_cutout(
        box_center(
            params.esp32_usb_opening_length,
            params.esp32_usb_opening_width,
            params.esp32_usb_opening_height,
            params.esp32_x + params.esp32_length / 2 + params.board_rail_thickness,
            params.esp32_y,
            floor_top_z + params.esp32_usb_opening_height / 2 + 2.0,
        )
    )
    add_cutout(
        box_center(
            params.esp32_usb_relief_depth,
            params.esp32_usb_relief_width,
            params.esp32_usb_relief_height,
            params.esp32_x + params.esp32_length / 2 + params.board_rail_thickness + params.esp32_usb_relief_depth / 2 - 2.0,
            params.esp32_y,
            floor_top_z + params.esp32_usb_relief_height / 2 + 2.0,
        )
    )

    for slot_x in (
        params.buck_x - params.buck_mount_slot_span_x / 2,
        params.buck_x + params.buck_mount_slot_span_x / 2,
    ):
        for slot_y in (
            params.buck_y - params.buck_mount_slot_span_y / 2,
            params.buck_y + params.buck_mount_slot_span_y / 2,
        ):
            add_cutout(
                box_center(
                    params.buck_mount_slot_length,
                    params.buck_mount_slot_width,
                    params.base_thickness + 1.0,
                    slot_x,
                    slot_y,
                    params.base_thickness / 2,
                )
            )

    for anchor_x, anchor_y in (
        (params.esp32_x + 18.0, params.esp32_y - 20.0),
        (params.buck_x + 14.0, params.buck_y + 18.0),
        (params.battery_x + 28.0, 0.0),
        (params.motor_mount_x - 26.0, 32.0),
        (params.motor_mount_x - 26.0, -32.0),
    ):
        for slot_y in (-2.5, 2.5):
            add_cutout(
                box_center(
                    params.wire_anchor_slot_length,
                    params.wire_anchor_slot_width,
                    params.base_thickness + 1.0,
                    anchor_x,
                    anchor_y + slot_y,
                    params.base_thickness / 2,
                )
            )

    add_cutout(
        box_center(
            params.wall_thickness + 2.0,
            params.sensor_wire_slot_width,
            params.sensor_wire_slot_height,
            front_sensor_wire_x,
            0,
            floor_top_z + params.sensor_wire_slot_height / 2 + 1.0,
        )
    )

    for slot_y in (
        -params.qtr_slot_spacing / 2,
        params.qtr_slot_spacing / 2,
    ):
        add_cutout(
            box_center(
                params.qtr_slot_width,
                params.qtr_slot_length,
                params.qtr_mount_height + 1.0,
                params.qtr_x,
                slot_y,
                floor_top_z + params.qtr_mount_height / 2,
            )
        )
    for slot_x in (
        params.vl53_x - params.vl53_slot_spacing / 2,
        params.vl53_x + params.vl53_slot_spacing / 2,
    ):
        add_cutout(
            box_center(
                params.vl53_slot_length,
                params.vl53_slot_width,
                params.vl53_mount_height + 1.0,
                slot_x,
                params.vl53_y,
                floor_top_z + params.vl53_mount_height / 2,
            )
        )

    ballast_slot_y = (
        params.front_ballast_y
        + params.front_ballast_width / 2
        + params.front_ballast_rail_thickness / 2
        + 1.5
    )
    ballast_slot_y_inner = (
        params.front_ballast_y
        - params.front_ballast_width / 2
        - params.front_ballast_rail_thickness / 2
        - 1.5
    )
    for direction in (1, -1):
        for slot_x in (
            params.front_ballast_x - params.front_ballast_length / 4,
            params.front_ballast_x + params.front_ballast_length / 4,
        ):
            add_cutout(
                box_center(
                    params.front_ballast_strap_slot_length,
                    params.front_ballast_strap_slot_width,
                    params.base_thickness + 1.0,
                    slot_x,
                    direction * ballast_slot_y,
                    params.base_thickness / 2,
                )
            )
            add_cutout(
                box_center(
                    params.front_ballast_strap_slot_length,
                    params.front_ballast_strap_slot_width,
                    params.base_thickness + 1.0,
                    slot_x,
                    direction * ballast_slot_y_inner,
                    params.base_thickness / 2,
                )
            )

    add_cutout(
        box_center(
            params.wall_thickness + 2.0,
            params.switch_slot_width,
            params.switch_slot_height,
            -half_length,
            0,
            floor_top_z + params.switch_slot_z,
        )
    )

    skid_x = -half_length + 16.0
    for skid_y in (-params.skid_hole_spacing / 2, params.skid_hole_spacing / 2):
        add_cutout(
            cylinder_min(
                params.skid_hole_diameter / 2,
                params.base_thickness + params.rear_bridge_height + 1.0,
                skid_x,
                skid_y,
                0,
            )
        )

    return chassis - cutouts


def build_rear_skid(params: ChassisParams):
    skid = box_min(
        params.skid_part_length,
        params.skid_part_width,
        params.skid_part_thickness,
        0,
        0,
        0,
    )

    cutouts = None

    def add_cutout(shape):
        nonlocal cutouts
        cutouts = shape if cutouts is None else cutouts + shape

    for slot_y in (-params.skid_hole_spacing / 2, params.skid_hole_spacing / 2):
        add_cutout(
            box_center(
                params.skid_slot_length,
                params.skid_slot_width,
                params.skid_part_thickness + 1.0,
                0,
                slot_y,
                params.skid_part_thickness / 2,
            )
        )

    front_x = params.skid_part_length / 2
    top_z = params.skid_part_thickness
    front_edges = [
        edge
        for edge in skid.edges()
        if abs(edge.center().X - front_x) < 0.001 and abs(edge.center().Z - top_z) < 0.001
    ]
    skid = chamfer(front_edges, params.skid_part_thickness - 0.5, 3.0)

    return skid - cutouts


def build_ballast_insert(params: ChassisParams):
    outer_length = params.front_ballast_length - 2 * params.front_ballast_insert_clearance
    outer_width = params.front_ballast_width - 2 * params.front_ballast_insert_clearance
    outer_height = min(
        params.front_ballast_height - params.front_ballast_insert_top_clearance,
        params.front_ballast_segment_face_width + params.front_ballast_insert_floor_thickness,
    )
    wall = params.front_ballast_insert_wall_thickness
    divider = params.front_ballast_insert_divider_thickness
    floor = params.front_ballast_insert_floor_thickness
    segments = params.front_ballast_segments_per_insert
    slot_width = (
        outer_width - 2 * wall - (segments - 1) * divider
    ) / segments
    slot_length = outer_length - 2 * wall
    wall_height = outer_height - floor

    insert = box_min(outer_length, outer_width, floor, 0, 0, 0)
    insert += box_min(outer_length, wall, wall_height, 0, outer_width / 2 - wall / 2, floor)
    insert += box_min(outer_length, wall, wall_height, 0, -outer_width / 2 + wall / 2, floor)
    insert += box_min(wall, outer_width, wall_height, outer_length / 2 - wall / 2, 0, floor)
    insert += box_min(wall, outer_width, wall_height, -outer_length / 2 + wall / 2, 0, floor)

    first_divider_y = -outer_width / 2 + wall + slot_width + divider / 2
    pitch = slot_width + divider
    for divider_index in range(segments - 1):
        divider_y = first_divider_y + divider_index * pitch
        insert += box_min(
            slot_length,
            divider,
            wall_height,
            0,
            divider_y,
            floor,
        )

    return insert


def export_chassis(params: ChassisParams):
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    chassis = build_chassis(params)
    skid = build_rear_skid(params)
    ballast_insert = build_ballast_insert(params)
    bbox = chassis.bounding_box()

    step_path = EXPORT_DIR / "sumobot_chassis.step"
    stl_path = EXPORT_DIR / "sumobot_chassis.stl"
    skid_step_path = EXPORT_DIR / "sumobot_rear_skid.step"
    skid_stl_path = EXPORT_DIR / "sumobot_rear_skid.stl"
    ballast_insert_step_path = EXPORT_DIR / "sumobot_ballast_insert.step"
    ballast_insert_stl_path = EXPORT_DIR / "sumobot_ballast_insert.stl"
    metadata_path = EXPORT_DIR / "sumobot_chassis_manifest.json"

    export_step(chassis, step_path)
    export_stl(chassis, stl_path)
    export_step(skid, skid_step_path)
    export_stl(skid, skid_stl_path)
    export_step(ballast_insert, ballast_insert_step_path)
    export_stl(ballast_insert, ballast_insert_stl_path)

    metadata = {
        "chosen_stack": "build123d 0.10.0",
        "exported_files": [
            step_path.name,
            stl_path.name,
            skid_step_path.name,
            skid_stl_path.name,
            ballast_insert_step_path.name,
            ballast_insert_stl_path.name,
        ],
        "legal_envelope_mm": {
            "length": round(bbox.max.X - bbox.min.X, 3),
            "width": round(bbox.max.Y - bbox.min.Y, 3),
            "height_estimate": round(bbox.max.Z - bbox.min.Z, 3),
        },
        "assumptions": {
            "motor_family": "TT DC gear motor 70 x 23 x 18 mm, with shaft center assumed 10.5 mm above the motor mount floor",
            "battery_pack": "7.4V Li-ion battery 70 x 40 x 20 mm",
            "bot_mcu_mount": "ESP32 DevKit V1 tray sized for 55 x 28 x 15 mm",
            "power_mount": "LM2596 buck converter tray sized for 45 x 22 x 15 mm",
            "battery_service": "battery bay includes side finger reliefs and a rear-left lead exit notch toward the power trench",
            "switch_type": "KCD1 rocker switch cutout 19 x 13 mm",
            "switch_guard": "rear protective ribs and roof extend the actual chassis length to 188 mm overall",
            "esp32_service": "USB service pocket sized for a common micro-USB cable head plus finger clearance",
            "board_retention": "ESP32 uses end-capture tabs plus strap retention; LM2596 gets adjustable mounting slots plus strap retention",
            "front_sensors": "QTR-8RC sensor shelf and VL53L0X sensor shelf included",
            "front_ballast": "paired ballast bays sit inside the front half behind the sensor deck, keeping the attack edge cleaner while allowing tunable steel or lead ballast",
            "ballast_insert": "separate printable insert sized around standard 1/4 oz steel wheel-weight segments, five segments per insert",
            "ballast_segment_reference": f"1/4 oz steel segment around {params.front_ballast_segment_length:.1f} x {params.front_ballast_segment_face_width:.1f} mm face, with thickness inferred near {params.front_ballast_segment_thickness_assumed:.2f} mm from mass and steel density",
            "rear_skid": "separate 2.5 mm wear skid part, intended for PTFE or UHMW and mounted with two M3 screws in slotted holes",
            "wheel_target": f"{params.wheel_diameter_assumption:.0f} mm diameter x {params.wheel_width_assumption:.0f} mm wide TT wheel",
        },
        "parameters_mm": asdict(params),
    }
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    return (
        step_path,
        stl_path,
        skid_step_path,
        skid_stl_path,
        ballast_insert_step_path,
        ballast_insert_stl_path,
        metadata_path,
    )


def main():
    params = ChassisParams()
    (
        step_path,
        stl_path,
        skid_step_path,
        skid_stl_path,
        ballast_insert_step_path,
        ballast_insert_stl_path,
        metadata_path,
    ) = export_chassis(params)
    print(f"Exported STEP: {step_path}")
    print(f"Exported STL: {stl_path}")
    print(f"Exported skid STEP: {skid_step_path}")
    print(f"Exported skid STL: {skid_stl_path}")
    print(f"Exported ballast insert STEP: {ballast_insert_step_path}")
    print(f"Exported ballast insert STL: {ballast_insert_stl_path}")
    print(f"Exported manifest: {metadata_path}")


if __name__ == "__main__":
    main()
