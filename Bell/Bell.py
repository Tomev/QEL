# A script that generates circuits preparing copies of a Bell state.

import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

import os, sys
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from methods import test_locally


def get_bell_circuits(circuits_copies_number: int = 50):
    qr = QuantumRegister(5)
    cr = ClassicalRegister(5)

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

    return circuits


print("Bell experiment start")

test_locally(get_bell_circuits())

print("Bell experiment finished")
