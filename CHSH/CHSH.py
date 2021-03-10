import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

from ..methods import test_locally, run_main_loop, test_locally_with_noise, add_measure_in_base


def get_chsh_circuits(steps=8):
    # Creating registers
    q = QuantumRegister(2)
    c = ClassicalRegister(2)

    # quantum circuit to make an entangled bell state
    bell = QuantumCircuit(q, c)
    bell.h(q[0])
    bell.cx(q[0], q[1])

    bases_to_measure = ['ZZ', 'ZX', 'XX', 'XZ']

    real_chsh_circuits = []

    for step in range(steps):

        theta = 2.0 * np.pi * step / steps

        bell_middle = QuantumCircuit(q, c)
        bell_middle.ry(theta, q[0])
        # bell_middle.barrier()

        barrier_bell_middle = QuantumCircuit(q, c)
        barrier_bell_middle.ry(theta, q[0])
        barrier_bell_middle.barrier()

        for b in bases_to_measure:
            new_circuit = bell + bell_middle
            new_circuit.name = 'CHSH_' + str(2 * step) + 'pi/' + str(steps)
            new_circuit = add_measure_in_base(new_circuit, b)

            barrier_new_circuit = bell + barrier_bell_middle
            barrier_new_circuit.name = 'CHSH_' + str(2 * step) + 'pi/' + str(steps) + '_B'
            barrier_new_circuit = add_measure_in_base(barrier_new_circuit, b)

            real_chsh_circuits.append(new_circuit)
            real_chsh_circuits.append(barrier_new_circuit)

    return real_chsh_circuits

# run_main_loop(get_chsh_circuits())
# test_locally(get_chsh_circuits(steps_number), use_mapping=True, save_to_file=True, number_of_simulations=100)
# test_locally_with_noise(get_chsh_circuits(steps_number))
