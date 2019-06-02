// According to https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5715115/

OPENQASM 2.0;
include "qelib1.inc";

// C3 gate: Toffoli controlled Z
// source: from ccx code (QASM specification)
//         H ccx H -> ccz
gate ccz a,b,c
{
cx b,c; tdg c;
cx a,c; t c;
cx b,c; tdg c;
cx a,c; t b; t c; //h c;
cx a,b; t a; tdg b;
cx a,b;
//h c;
}

// XH combined gate
//gate g_xh a { h a; z a; }
gate xh a { u2(pi,pi) a; }

// HX combined gate
//gate g_hx a { z a; h a; }
gate hx a { u2(0,0) a; }

// XHX combined gate
//gate g_xhx a { z a; h a; z a; }
gate xhx a { u2(-pi,0) a; }

qreg q[3];
creg c[3];

// h q[0]; x q[0];
hx q[0];

// h q[1]; x q[1];
hx q[1];

h q[2];

ccz q[0], q[1], q[2];

// x q[0]; h q[0]; x q[0];
xhx q[0];

// x q[1]; h q[1]; x q[1];
xhx q[1];

// h q[2]; x q[2];
hx q[2];

ccz q[0], q[1], q[2];

// x q[0]; h q[0]; x q[0];
xhx q[0];

// x q[1]; h q[1]; x q[1];
xhx q[1];

// x q[2]; h q[2];
xh q[2];

ccz q[0], q[1], q[2];

// x q[0]; h q[0]; x q[0];
xhx q[0];

//x q[1]; h q[1]; x q[1];
xhx q[1];

// h q[2]; x q[2];
hx q[2];

ccz q[0], q[1], q[2];

// x q[0]; h q[0];
// x q[1]; h q[1];
// x q[2]; h q[2];
xh q;

measure q -> c;
