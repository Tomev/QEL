import numpy as np
import sys
sys.path.append('..')
from methods import test_locally, run_main_loop
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

steps_number = 8


def get_chsh_circuits(steps=10):
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

    measure = {'ZZ': measure_zz, 'ZX': measure_zx, 'XX': measure_xx, 'XZ': measure_xz}

    real_chsh_circuits = []

    for step in range(steps):

        theta = 2.0 * np.pi * step / steps

        bell_middle = QuantumCircuit(q, c)
        bell_middle.ry(theta, q[0])
        # bell_middle.barrier()

        barrier_bell_middle = QuantumCircuit(q, c)
        barrier_bell_middle.ry(theta, q[0])
        barrier_bell_middle.barrier()
        
        for m in measure.keys():

            new_circuit = bell + bell_middle + measure[m]
            new_circuit.name = 'CHSH_' + str(2 * step) + 'pi/' + str(steps) + '_' + m

            barrier_new_circuit = bell + barrier_bell_middle + measure[m]
            barrier_new_circuit.name = 'CHSH_' + str(2 * step) + 'pi/' + str(steps) + '_' + m + '_B'

            real_chsh_circuits.append(new_circuit)
            real_chsh_circuits.append(barrier_new_circuit)

    print("Number of circuits: " + str(len(real_chsh_circuits)))

    return real_chsh_circuits


run_main_loop(get_chsh_circuits(steps_number))
# test_locally(get_chsh_circuits(steps_number))
