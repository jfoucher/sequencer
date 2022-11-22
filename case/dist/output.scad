
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
$fn = 64;
union()
{
  union()
  {
    difference()
    {
      minkowski()
      {
        cube(size = [190.5, 70, 20], center = true);
        cylinder(h = 5, r = 5, center = true);
      }
      minkowski()
      {
        cube(size = [184.5, 64, 16], center = true);
        cylinder(h = 5, r = 1, center = true);
      }
      translate(v = [0, 0, 10])
      {
        cube(size = [266.7, 100, 30], center = true);
      }
      translate(v = [0, 0, -10])
      {
        intersection()
        {
          translate(v = [-91.25, -31, 0])
          {
            union()
            {
              translate(v = [0, 0, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [0, 8, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [0, 16, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [0, 24, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [0, 32, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [0, 40, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [0, 48, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [0, 56, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [0, 64, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [8, 4, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [8, 12, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [8, 20, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [8, 28, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [8, 36, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [8, 44, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [8, 52, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [8, 60, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [8, 68, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [16, 0, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [16, 8, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [16, 16, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [16, 24, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [16, 32, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [16, 40, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [16, 48, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [16, 56, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [16, 64, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [24, 4, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [24, 12, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [24, 20, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [24, 28, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [24, 36, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [24, 44, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [24, 52, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [24, 60, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [24, 68, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [32, 0, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [32, 8, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [32, 16, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [32, 24, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [32, 32, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [32, 40, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [32, 48, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [32, 56, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [32, 64, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [40, 4, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [40, 12, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [40, 20, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [40, 28, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [40, 36, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [40, 44, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [40, 52, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [40, 60, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [40, 68, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [48, 0, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [48, 8, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [48, 16, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [48, 24, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [48, 32, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [48, 40, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [48, 48, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [48, 56, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [48, 64, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [56, 4, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [56, 12, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [56, 20, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [56, 28, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [56, 36, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [56, 44, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [56, 52, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [56, 60, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [56, 68, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [64, 0, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [64, 8, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [64, 16, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [64, 24, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [64, 32, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [64, 40, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [64, 48, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [64, 56, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [64, 64, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [72, 4, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [72, 12, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [72, 20, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [72, 28, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [72, 36, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [72, 44, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [72, 52, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [72, 60, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [72, 68, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [80, 0, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [80, 8, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [80, 16, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [80, 24, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [80, 32, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [80, 40, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [80, 48, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [80, 56, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [80, 64, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [88, 4, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [88, 12, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [88, 20, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [88, 28, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [88, 36, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [88, 44, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [88, 52, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [88, 60, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [88, 68, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [96, 0, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [96, 8, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [96, 16, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [96, 24, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [96, 32, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [96, 40, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [96, 48, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [96, 56, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [96, 64, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [104, 4, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [104, 12, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [104, 20, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [104, 28, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [104, 36, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [104, 44, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [104, 52, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [104, 60, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [104, 68, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [112, 0, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [112, 8, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [112, 16, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [112, 24, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [112, 32, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [112, 40, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [112, 48, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [112, 56, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [112, 64, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [120, 4, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [120, 12, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [120, 20, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [120, 28, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [120, 36, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [120, 44, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [120, 52, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [120, 60, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [120, 68, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [128, 0, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [128, 8, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [128, 16, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [128, 24, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [128, 32, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [128, 40, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [128, 48, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [128, 56, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [128, 64, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [136, 4, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [136, 12, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [136, 20, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [136, 28, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [136, 36, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [136, 44, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [136, 52, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [136, 60, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [136, 68, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [144, 0, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [144, 8, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [144, 16, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [144, 24, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [144, 32, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [144, 40, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [144, 48, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [144, 56, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [144, 64, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [152, 4, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [152, 12, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [152, 20, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [152, 28, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [152, 36, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [152, 44, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [152, 52, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [152, 60, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [152, 68, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [160, 0, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [160, 8, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [160, 16, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [160, 24, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [160, 32, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [160, 40, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [160, 48, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [160, 56, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [160, 64, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [168, 4, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [168, 12, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [168, 20, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [168, 28, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [168, 36, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [168, 44, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [168, 52, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [168, 60, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [168, 68, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [176, 0, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [176, 8, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [176, 16, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [176, 24, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [176, 32, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [176, 40, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [176, 48, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [176, 56, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [176, 64, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [184, 4, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [184, 12, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [184, 20, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [184, 28, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [184, 36, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [184, 44, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [184, 52, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [184, 60, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
              translate(v = [184, 68, 0])
              {
                cylinder(h = 8, r = 4, center = true, $fn = 6);
              }
            }
          }
          cube(size = [182.5, 62, 8], center = true);
        }
      }
      translate(v = [95.25, 35, 0])
      {
        cylinder(h = 30, r = 2, center = true);
      }
      translate(v = [95.25, -35, 0])
      {
        cylinder(h = 30, r = 2, center = true);
      }
      translate(v = [-95.25, 35, 0])
      {
        cylinder(h = 30, r = 2, center = true);
      }
      translate(v = [-95.25, -35, 0])
      {
        cylinder(h = 30, r = 2, center = true);
      }
    }
  }
}
