// GHOST text plate — place this ON TOP of TapaSumo in your slicer
// Dimensions: fits centered on a 112x112mm cover
// Height: 3mm raised text on a 1mm base plate

translate([0, 0, 0])
union() {
    // Base plate
    cube([90, 20, 1]);

    // Raised GHOST letters
    translate([45, 10, 1])
        linear_extrude(height=3)
            text("GHOST",
                 size=14,
                 font="Liberation Sans:style=Bold",
                 halign="center",
                 valign="center");
}
