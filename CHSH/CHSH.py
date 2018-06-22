from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from methods import run_main_loop
import numpy as np


def get_chsh_circuits():
    # Creating registers
    q = QuantumRegister(2)
    c = ClassicalRegister(2)

    # quantum circuit to make an entangled bell state
    bell = QuantumCircuit(q, c)
    bell.h(q[0])
    bell.cx(q[0], q[1])

    # quantum circuit to measure q in the standard basis
    measure_zz = QuantumCircuit(q, c)
    measure_zz.measure(q[0], c[0])
    measure_zz.measure(q[1], c[1])

    # quantum circuit to measure q in the superposition basis
    measure_xx = QuantumCircuit(q, c)
    measure_xx.h(q[0])
    measure_xx.h(q[1])
    measure_xx.measure(q[0], c[0])
    measure_xx.measure(q[1], c[1])

    # quantum circuit to measure ZX
    measure_zx = QuantumCircuit(q, c)
    measure_zx.h(q[0])
    measure_zx.measure(q[0], c[0])
    measure_zx.measure(q[1], c[1])

    # quantum circuit to measure XZ
    measure_xz = QuantumCircuit(q, c)
    measure_xz.h(q[1])
    measure_xz.measure(q[0], c[0])
    measure_xz.measure(q[1], c[1])

    measure = [measure_zz, measure_zx, measure_xx, measure_xz]

    real_chsh_circuits = []
    real_x = []

    real_steps = 10

    for step in range(real_steps):

        theta = 2.0 * np.pi * step / 10
        bell_middle = QuantumCircuit(q, c)
        bell_middle.ry(theta, q[0])

        for m in measure:
            real_chsh_circuits.append(bell + bell_middle + m)

        real_x.append(theta)

    return real_chsh_circuits


# Prepare circuits here.
chsh_circuits = get_chsh_circuits()

print('Circuit prepared for execution.')

# Assign circuits to run here.
run_main_loop(chsh_circuits)
