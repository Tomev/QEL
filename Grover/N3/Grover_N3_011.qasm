// According to https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5715115/

OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];
creg c[5];

// Init
h q[0];
h q[1];
h q[2];

//BEGIN Oracle for |011>
x q[0];

// CCZ using CCX
h q[2];
ccx q[0], q[1], q[2];
h q[2];

x q[0];
// END Oracle for |011>

// BEGIN Amplification
h q[0];
h q[1];
h q[2];
x q[0];
x q[1];
x q[2];
h q[2];
ccx q[0], q[1], q[2];
h q[2];
x q[0];
x q[1];
x q[2];
h q[0];
h q[1];
h q[2];
// END Amplification
 
// And now repeat this (everything besides initialization)
 
//BEGIN Oracle for |011>
x q[0];

// CCZ using CCX
h q[2];
ccx q[0], q[1], q[2];
h q[2];

x q[0];
// END Oracle for |011>

// BEGIN Amplification
h q[0];
h q[1];
h q[2];
x q[0];
x q[1];
x q[2];
h q[2];
ccx q[0], q[1], q[2];
h q[2];
x q[0];
x q[1];
x q[2];
h q[0];
h q[1];
h q[2];
// END Amplification 

measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
