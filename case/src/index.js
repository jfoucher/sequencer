const fs = require('fs');
const { cylinder, difference, sphere, cube, polygon, union, hull, intersection, multmatrix, minkowski, mirror, linear_extrude, text_3d, rounded_cube, knurled_cyl } = require('scad-js');


const size = 20;
const hole = size / 2;
const cylinderHeight = size * 2.5;

let totalN = 10;
let actualN = 20;

let thickness = 4;

const switchHeight = 14.4
const switchWidth = 14.4

const mountWidth = switchWidth + 3;
const mountHeight = switchHeight + 3;
const keyhole = cube([switchHeight, switchWidth, thickness*4])

const keyPitch = 19.05;
const keyCols = 12;
const keyRows = 5;

const plh = union(
  cube([mountWidth, 1.5, 4]).translate([0, switchHeight/2 + 1.5/2,  2]),
  cube([1.5, mountHeight, 4]).translate([switchWidth/2 + 1.5/2, 0, 2]),
  hull(
    cylinder(2.75, 1, 1).rotate([90, 0, 0]).translate([switchWidth/2, 0, 1]),
    cube([1.5, 2.75, 4]).translate([switchWidth/2 + 1.5/2, 0,2 ])
  ),
)

const switchHole = union(plh, plh.mirror([1, 0, 0]).mirror([0, 1, 0]))

keys = union(...[0, 1, 2, 3, 4, 5, 6, 7].map(n => switchHole.translate([n*keyPitch - 4.5*keyPitch, 0, 16])))
holes = union(...[0, 1, 2, 3, 4, 5, 6, 7].map(n => keyhole.translate([n*keyPitch - 4.5*keyPitch, 0, 16])))
leds  = union(...[0, 1, 2, 3, 4, 5, 6, 7].map(n => cylinder(30, 2.5).translate([n*keyPitch - 4.5*keyPitch, 0, 16])))
knob_shaft_radius = 3;
knob_shaft_flat = 1.5;
knob_shaft_length = 5;
knob_height = 15;
knob_radius = 15;
tol = 0.2;
let knob = union(
  difference(
    knurled_cyl(knob_height, knob_radius*2, 3, 3, 1, 2, 40),
    cylinder(2.1, knob_radius-3).translate([0, 0, 1]),
difference(
      cylinder(knob_shaft_length+1, knob_shaft_radius+tol).translate([0, 0, 4.5]),
      cube([8, 8, 8]).translate([4+knob_shaft_flat, 0, 4])
    )
    
    
  ),
  
)

const top_angle = 5

let screw_hole = cylinder(6.1, 2.3).translate([0, 0, 3])

const top = 
difference(
difference(
union(
  //knob.translate([77, -15, 22]),
  union(
  difference(

      minkowski(
        cube([keyPitch*10, 70, 30]),
        sphere(5)
      ),
      

    minkowski(
      cube([keyPitch*10-6, 64, 22]),
      sphere(1)
    ),
    
    
  ),
  cylinder(30, 5).translate([keyPitch*5, 35, 0]),
  cylinder(30, 5).translate([keyPitch*5, -35, 0]),
  cylinder(30, 5).translate([-keyPitch*5, 35, 0]),
  cylinder(30, 5).translate([-keyPitch*5, -35, 0]),
  ).multmatrix([[1, 0, 0, 0], [0, 1, Math.sin(top_angle*Math.PI/180), -2], [0, 0, 1, 0]]),
  keys.translate([0, -22, 0]),
  keys.translate([0, 12, 0]),
  
),

    holes.translate([0, -22, 0]),
    holes.translate([0, 12, 0]),
    leds.translate([0, -8, 0]),
    leds.translate([0, 27, 0]),
    // rotary encoder hole
    cylinder(50, 3.6).translate([77, -15, 20]),
    cube([10, 40, 5]).translate([77, 25, 2]),
    //cylinder(50, 4).scale([1.5, 1, 1]).rotate([90, 0, 0]).translate([77, 15, 0]),
    cylinder(50, 4).rotate([90, 0, 0]).translate([40, 15, 4]),
    cylinder(50, 4).rotate([90, 0, 0]).translate([20, 15, 4]),
    cube([25, 16, 12]).translate([77, 28, 0]),
    cube([13.5, 15.5, 20]).translate([77, -15, 6]),
).rotate([top_angle, 0, 0]),
cube([keyPitch*20, 100, 30]).translate([0, 0, -15]),
screw_hole.translate([keyPitch*5, 33, 0]),
screw_hole.translate([keyPitch*5, -37, 0]),
screw_hole.translate([-keyPitch*5, 33, 0]),
screw_hole.translate([-keyPitch*5, -37, 0]),
)


const output = top

const knurled_cylinder_module = `
/*
 * knurledFinishLib.scad
 * 
 * Written by aubenc @ Thingiverse
 *
 * This script is licensed under the Public Domain license.
 *
 * http://www.thingiverse.com/thing:9095
 *
 * Usage:
 *
 *    knurled_cyl( Knurled cylinder height,
 *                 Knurled cylinder outer diameter,
 *                 Knurl polyhedron width,
 *                 Knurl polyhedron height,
 *                 Knurl polyhedron depth,
 *                 Cylinder ends smoothed height,
 *                 Knurled surface smoothing amount );
 */
module knurled_cyl(chg, cod, cwd, csh, cdp, fsh, smt)
{
    cord=(cod+cdp+cdp*smt/100)/2;
    cird=cord-cdp;
    cfn=round(2*cird*PI/cwd);
    clf=360/cfn;
    crn=ceil(chg/csh);

    intersection()
    {
        shape(fsh, cird, cord-cdp*smt/100, cfn*4, chg);

        translate([0,0,-(crn*csh-chg)/2])
          knurled_finish(cord, cird, clf, csh, cfn, crn);
    }
}

module shape(hsh, ird, ord, fn4, hg)
{
        union()
        {
            cylinder(h=hsh, r1=ird, r2=ord, $fn=fn4, center=false);

            translate([0,0,hsh-0.002])
              cylinder(h=hg-2*hsh+0.004, r=ord, $fn=fn4, center=false);

            translate([0,0,hg-hsh])
              cylinder(h=hsh, r1=ord, r2=ird, $fn=fn4, center=false);
        }

}

module knurled_finish(ord, ird, lf, sh, fn, rn)
{
    for(j=[0:rn-1])
    
    {
      h0=sh*j;
      h1=sh*(j+1/2);
      h2=sh*(j+1);
        for(i=[0:fn-1])
        
        {
          lf0=lf*i;
        lf1=lf*(i+1/2);
        lf2=lf*(i+1);
            polyhedron(
                points=[
                     [ 0,0,h0],
                     [ ord*cos(lf0), ord*sin(lf0), h0],
                     [ ird*cos(lf1), ird*sin(lf1), h0],
                     [ ord*cos(lf2), ord*sin(lf2), h0],

                     [ ird*cos(lf0), ird*sin(lf0), h1],
                     [ ord*cos(lf1), ord*sin(lf1), h1],
                     [ ird*cos(lf2), ird*sin(lf2), h1],

                     [ 0,0,h2],
                     [ ord*cos(lf0), ord*sin(lf0), h2],
                     [ ird*cos(lf1), ird*sin(lf1), h2],
                     [ ord*cos(lf2), ord*sin(lf2), h2]
                    ],
                faces=[
                     [0,1,2],[2,3,0],
                     [1,0,4],[4,0,7],[7,8,4],
                     [8,7,9],[10,9,7],
                     [10,7,6],[6,7,0],[3,6,0],
                     [2,1,4],[3,2,6],[10,6,9],[8,9,4],
                     [4,5,2],[2,5,6],[6,5,9],[9,5,4]
                    ],
                convexity=5);
         }
    }
}
`

const string = knurled_cylinder_module + output.serialize({ $fn: 64 })

fs.writeFileSync('./dist/output.scad', string);