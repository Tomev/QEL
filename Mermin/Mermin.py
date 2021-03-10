import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

from ..methods import run_main_loop_with_chsh_test, test_locally, add_measure_in_base, draw_circuit

mermin_quantum_register = QuantumRegister(3)
c3 = ClassicalRegister(3)
selected_mermin_bases = ['XXX', 'YYX', 'YXY', 'XYY']
# topology_qubits_order = [1, 0, 2]  # For T topology, like QX London
topology_qubits_order = [0, 1, 2]  # For star topology, like QX2


def create_ghz_state():
    ghz3 = QuantumCircuit(mermin_quantum_register, c3)
    ghz3.h(mermin_quantum_register[topology_qubits_order[0]])
    ghz3.cx(mermin_quantum_register[topology_qubits_order[0]], mermin_quantum_register[topology_qubits_order[1]])
    ghz3.cx(mermin_quantum_register[topology_qubits_order[0]], mermin_quantum_register[topology_qubits_order[2]])
    ghz3.barrier()
    return ghz3


def add_measurements_in_selected_bases(circuits: list):
    circuits_with_measurements = []
    for base in selected_mermin_bases:
        for circuit in circuits:
            circuits_with_measurements.append(add_measure_in_base(circuit.copy(), base))
    return circuits_with_measurements


def apply_symmetric_rz_rotations(circuit: QuantumCircuit, steps_number: int):
    rotated_states = []
    for step in range(steps_number):
        theta = 2.0 * np.pi * step / steps_number
        rotated_state = circuit.copy()
        rotated_state.rz(theta / 3, mermin_quantum_register[0])
        rotated_state.rz(theta / 3, mermin_quantum_register[1])
        rotated_state.rz(theta / 3, mermin_quantum_register[2])
        rotated_state.barrier()
        rotated_states.append(rotated_state)
    return rotated_states


def name_circuits(circuits: list):
    for step in range(len(circuits)):
        circuits[step].name = 'Mermin_' + str(2 * step) + 'pi/' + str(len(circuits)) + '_B'


def get_mermin_circuits(steps=8):
    mermin_circuit = create_ghz_state()
    mermin_circuit.name = 'Mermin_B'
    rotated_states = apply_symmetric_rz_rotations(mermin_circuit, steps)
    name_circuits(rotated_states)
    mermin_circuits = add_measurements_in_selected_bases(rotated_states)
    return mermin_circuits


def get_mermin_test_circuits():
    mermin_test_base_circuits = create_ghz_state()
    mermin_test_base_circuits.name = "Mermin-test"
    mermin_test_circuits = add_measurements_in_selected_bases([mermin_test_base_circuits])
    return mermin_test_circuits


# run_main_loop_with_chsh_test(get_mermin_circuits())
# test_locally(get_mermin_circuits(), use_mapping=True, save_to_file=True, number_of_simulations=1)
# draw_circuit(get_mermin_circuits()[0])
test_locally(get_mermin_circuits())
