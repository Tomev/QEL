import numpy as np
import sys

sys.path.append('..')
from methods import test_locally, run_main_loop, test_locally_with_noise, add_measure_in_base, draw_circuit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

selected_chsh_bases = ['YY', 'YX', 'XX', 'XY']
chsh_quantum_register = QuantumRegister(2)
chsh_classical_register = ClassicalRegister(2)


def create_bell_state():
    bell = QuantumCircuit(chsh_quantum_register, chsh_classical_register)
    bell.h(chsh_quantum_register[0])
    bell.cx(chsh_quantum_register[0], chsh_quantum_register[1])
    bell.x(chsh_quantum_register[0])
    bell.barrier()
    return bell


def apply_rz_rotations(circuit: QuantumCircuit, steps_number: int):
    rotated_states = []
    for step in range(steps_number):
        theta = 2.0 * np.pi * step / steps_number
        rotated_state = circuit.copy()
        rotated_state.rz(-theta, chsh_quantum_register[0])
        rotated_state.barrier()
        rotated_states.append(rotated_state)
    return rotated_states


def name_circuits(circuits: list):
    for step in range(len(circuits)):
        circuits[step].name = 'CHSH_' + str(2 * step) + 'pi/' + str(len(circuits)) + '_B'


def add_measurements_in_selected_bases(circuits: list):
    circuits_with_measurements = []
    for base in selected_chsh_bases:
        for circuit in circuits:
            circuits_with_measurements.append(add_measure_in_base(circuit.copy(), base))
    return circuits_with_measurements


def get_chsh_circuits(steps=8):
    bell_state = create_bell_state()
    rotated_states = apply_rz_rotations(bell_state, steps)
    name_circuits(rotated_states)
    chsh_circuits = add_measurements_in_selected_bases(rotated_states)
    return chsh_circuits


def get_chsh_test_circuits():
    bell = create_bell_state()
    bell.rz(-np.pi / 4, chsh_quantum_register[0])
    bell.barrier()
    chsh_circuits = add_measurements_in_selected_bases([bell])

    # Set circuits names.
    chsh_circuits[0].name = 'CHSH-test_YY'
    chsh_circuits[1].name = 'CHSH-test_YX'
    chsh_circuits[2].name = 'CHSH-test_XX'
    chsh_circuits[3].name = 'CHSH-test_XY'

    return chsh_circuits


def apply_symmetric_rz_rotations(circuit: QuantumCircuit, steps_number: int):
    rotated_states = []
    for step in range(steps_number):
        theta = 2.0 * np.pi * step / steps_number
        rotated_state = circuit.copy()
        rotated_state.rz(theta / 2, chsh_quantum_register[0])
        rotated_state.rz(-theta / 2, chsh_quantum_register[1])
        rotated_state.barrier()
        rotated_states.append(rotated_state)
    return rotated_states


def get_symmetric_chsh_circuits(steps=8):
    bell_state = create_bell_state()
    rotated_states = apply_symmetric_rz_rotations(bell_state, steps)
    name_circuits(rotated_states)
    chsh_circuits = add_measurements_in_selected_bases(rotated_states)
    return chsh_circuits


def get_symmetric_chsh_test_circuits():
    bell = create_bell_state()
    bell.rz(np.pi / 8, chsh_quantum_register[0])
    bell.rz(-np.pi / 8, chsh_quantum_register[1])
    bell.barrier()
    chsh_circuits = add_measurements_in_selected_bases([bell])

    # Set circuits names.
    chsh_circuits[0].name = 'CHSH-test_YY'
    chsh_circuits[1].name = 'CHSH-test_YX'
    chsh_circuits[2].name = 'CHSH-test_XX'
    chsh_circuits[3].name = 'CHSH-test_XY'

    return chsh_circuits


draw_circuit(get_symmetric_chsh_test_circuits()[3])

# run_main_loop(get_chsh_circuits())
# test_locally(get_chsh_circuits(), use_mapping=True, save_to_file=True, number_of_simulations=1)
# test_locally_with_noise(get_chsh_circuits(steps_number))
