// Using mathematica notation.
// Composer address to look into available matrices (especially U):
// https://quantumexperience.ng.bluemix.net/qx/editor

// U_2 = u3(pi/2, phi, lambda) = 1 / sqrt(2) {{1,-exp(i lambda)}, {exp(i phi), exp(i(phi + lambda))}}

// U_3 = u3(theta, phi, lambda) = {{cos(theta/2), -exp(i lambda) sin(theta / 2)}, {exp(i phi) sin(theta/2), exp(i(lambda + phi))sincos(theta/2) }}

OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];
creg c[5];

// HX = u3(pi / 2, pi, pi) = 1 / sqrt(2) {{1,1}, {-1,1}}
//h q[0];
//x q[0];
u3(pi / 2, pi, pi) q[0];

// HX = u3(pi / 2, pi, pi) = 1 / sqrt(2) {{1,1}, {-1,1}}
//h q[1];
//x q[1];
u3(pi / 2, pi, pi) q[1];

// HH = Id
//h q[2];
//h q[2];

ccx q[0], q[1], q[2];

// XHX = u3(5/2 pi, pi, 0) =  1 / sqrt(2) {{-1,1}, {1,1}}
//x q[0];
//h q[0];
//x q[0];
u3(5/2 pi, pi, 0) q[0];

// XHX = u3(5/2 pi, pi, 0) =  1 / sqrt(2) {{-1,1}, {1,1}}
//x q[1];
//h q[1];
//x q[1];
u3(5/2 pi, pi, 0) q[1];

// HH = Id
//h q[2];
//h q[2];

// XH = u3(pi/2, 0, 0) = 1 / sqrt(2) {{1,-1}, {1,1}}
//x q[2];
//h q[2];
u3(pi/2, 0, 0) q[2];

ccx q[0], q[1], q[2];

// XHX = u3(5/2 pi, pi, 0) =  1 / sqrt(2) {{-1,1}, {1,1}}
//x q[0];
//h q[0];
//x q[0];
u3(5/2 pi, pi, 0) q[0];

// XHX = u3(5/2 pi, pi, 0) =  1 / sqrt(2) {{-1,1}, {1,1}}
//x q[1];
//h q[1];
//x q[1];
u3(5/2 pi, pi, 0) q[1];

// HX = u3(pi / 2, pi, pi) = 1 / sqrt(2) {{1,1}, {-1,1}}
//h q[2];
//x q[2];
u3(pi / 2, pi, pi) q[2];

// HH = Id
//h q[2];
//h q[2];

ccx q[0], q[1], q[2];

// XHX = u3(5/2 pi, pi, 0) =  1 / sqrt(2) {{-1,1}, {1,1}}
//x q[0];
//h q[0];
//x q[0];
u3(5/2 pi, pi, 0) q[0];

// XHX = u3(5/2 pi, pi, 0) =  1 / sqrt(2) {{-1,1}, {1,1}}
//x q[1];
//h q[1];
//x q[1];
u3(5/2 pi, pi, 0) q[1];

// HH = Id
//h q[2];
//h q[2];

// XH = u3(pi/2, 0, 0) = 1 / sqrt(2) {{1,-1}, {1,1}}
//x q[2];
//h q[2];
u3(pi/2, 0, 0) q[2];

ccx q[0], q[1], q[2];

// XH = u3(pi/2, 0, 0) = 1 / sqrt(2) {{1,-1}, {1,1}}
//x q[0];
//h q[0];
u3(pi/2, 0, 0) q[0];

// XH = u3(pi/2, 0, 0) = 1 / sqrt(2) {{1,-1}, {1,1}}
//x q[1];
//h q[1];
u3(pi/2, 0, 0) q[1];

// HXH = Z
//h q[2];
//x q[2];
//h q[2];
z q[2];

measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];