$fn = 96;

module wheel(side_y) {
    color([0.11, 0.12, 0.14])
    translate([-18, side_y, 14.5])
    rotate([90, 0, 0])
    cylinder(h = 26, r = 32.5, center = true);
}

module motor(side_y) {
    color([0.73, 0.76, 0.79])
    translate([-18, side_y, 13])
    cube([70, 23, 18], center = true);
}

module board(position, size, tint) {
    color(tint)
    translate(position)
    cube(size, center = true);
}

color([0.86, 0.88, 0.90])
import("../exports/sumobot_chassis.stl", convexity = 10);

wheel(97);
wheel(-97);

motor(69.5);
motor(-69.5);

board([18, 0, 14], [70, 40, 20], [0.92, 0.55, 0.18, 0.75]);
board([-22, 27, 11.5], [55, 28, 15], [0.14, 0.58, 0.23, 0.92]);
board([-22, -25, 11.5], [45, 22, 15], [0.16, 0.48, 0.84, 0.92]);
board([50, 0, 6.5], [75, 13, 2.5], [0.08, 0.08, 0.08, 0.95]);
board([28, 0, 12], [25, 13, 8], [0.72, 0.18, 0.18, 0.92]);
