import numpy as np
import sys
sys.path.append('../..')
from methods import test_locally, run_main_loop
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def get_chsh_circuits():
    # Creating registers
    q = QuantumRegister(2)
    c = ClassicalRegister(2)

    # Quantum circuit to make an entangled bell state.
    bell = QuantumCircuit(q, c)
    bell.h(q[0])
    bell.cx(q[0], q[1])

    # Quantum circuit to measure q in the standard basis.
    measure_zz = QuantumCircuit(q, c)
    measure_zz.measure(q[0], c[0])
    measure_zz.measure(q[1], c[1])

    # Quantum circuit to measure q in the superposition basis.
    measure_xx = QuantumCircuit(q, c)
    measure_xx.h(q[0])
    measure_xx.h(q[1])
    measure_xx.measure(q[0], c[0])
    measure_xx.measure(q[1], c[1])

    # Quantum circuit to measure ZX.
    measure_zx = QuantumCircuit(q, c)
    measure_zx.h(q[0])
    measure_zx.measure(q[0], c[0])
    measure_zx.measure(q[1], c[1])

    # Quantum circuit to measure XZ.
    measure_xz = QuantumCircuit(q, c)
    measure_xz.h(q[1])
    measure_xz.measure(q[0], c[0])
    measure_xz.measure(q[1], c[1])

    measure_circuits = [measure_zz, measure_zx, measure_xx, measure_xz]
    measure_names = ["ZZ", "ZX", "XX", "XZ"]

    real_chsh_circuits = []
    real_x = []

    real_steps = 10

    for step in range(real_steps):

        theta = 2.0 * np.pi * step / 10.0
        bell_middle = QuantumCircuit(q, c)
        bell_middle.ry(theta, q[0])

        for i in range(len(measure_circuits)):
            real_chsh_circuits.append(bell + bell_middle + measure_circuits[i])
            real_chsh_circuits[len(real_chsh_circuits) - 1].name = "CHSH_" + measure_names[i] + "_" + str(theta)[:4]

        real_x.append(theta)

    return real_chsh_circuits


#run_main_loop(get_chsh_circuits())
test_locally(get_chsh_circuits())
