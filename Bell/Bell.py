# A script that generates copies of Bell state preparing circuits.

import sys

sys.path.append('..\\')
import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from methods import test_locally, run_main_loop_with_chsh_test

circuits_copies_number = 50

qr = QuantumRegister(5)
cr = ClassicalRegister(5)


print("Bell experiment start")

circuits = []

# Circuits preparation
for i in range(0, circuits_copies_number):

    qc = QuantumCircuit(qr, cr)
    qc.h(qr[2])
    qc.cx(qr[2], qr[0])
    qc.cx(qr[2], qr[4])
    qc.h(qr[2])
    qc.ry(np.pi / 4, qr[0])
    qc.measure(qr, cr)

    circuits.append(qc)
    circuits[i].name = "Bell_" + str(i)

# test_locally(circuits)
run_main_loop_with_chsh_test(circuits)

print("Bell experiment finished")


