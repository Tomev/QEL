import sys
sys.path.append('../')
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from methods import run_main_loop_with_chsh_test, test_locally, add_measure_in_base, draw_circuit
import numpy as np


def get_mermin_circuits(steps=8):

    # 3 - qubits
    # quantum circuit to make GHZ state 
    q3 = QuantumRegister(3)
    c3 = ClassicalRegister(3)

    topology_qubits_order = [1, 0, 2]      #  For T topology, like QX London
    #topology_qubits_order = [0, 1, 2]      #  For star topology, like QX2

    ghz3 = QuantumCircuit(q3, c3)
    ghz3.h(q3[topology_qubits_order[0]])
    ghz3.cx(q3[topology_qubits_order[0]], q3[topology_qubits_order[1]])
    ghz3.cx(q3[topology_qubits_order[0]], q3[topology_qubits_order[2]])
    ghz3.name = 'Mermin'

    bghz3 = QuantumCircuit(q3, c3)
    bghz3.h(q3[topology_qubits_order[0]])
    bghz3.cx(q3[topology_qubits_order[0]], q3[topology_qubits_order[1]])
    bghz3.cx(q3[topology_qubits_order[0]], q3[topology_qubits_order[2]])
    bghz3.barrier()
    bghz3.name = 'Mermin_B'

    bases = ['XXX', 'YYX', 'YXY', 'XYY']
    circuits = []

    for step in range(steps):

        theta = 2.0 * np.pi * step / steps

        ghz_middle = QuantumCircuit(q3, c3)
        ghz_middle.rz(theta, q3[topology_qubits_order[1]])

        barrier_ghz_middle = QuantumCircuit(q3, c3)
        barrier_ghz_middle.rz(theta, q3[topology_qubits_order[1]])
        barrier_ghz_middle.barrier()

        for b in bases:

            new_circuit = ghz3 + ghz_middle
            new_circuit.name = 'Mermin_' + str(2 * step) + 'pi/' + str(steps)
            new_circuit = add_measure_in_base(new_circuit, b)

            barrier_new_circuit = bghz3 + barrier_ghz_middle
            barrier_new_circuit.name = 'Mermin_' + str(2 * step) + 'pi/' + str(steps) + '_B'
            barrier_new_circuit = add_measure_in_base(barrier_new_circuit, b)

            circuits.append(new_circuit)
            circuits.append(barrier_new_circuit)

    '''
    for b in bases:
        circuits.append(add_measure_in_base(ghz3.copy(), b))
    for b in bases:
        circuits.append(add_measure_in_base(bghz3.copy(), b))
    '''

    return circuits


#run_main_loop_with_chsh_test(get_mermin_circuits())
#test_locally(get_mermin_circuits(), use_mapping=True, save_to_file=True, number_of_simulations=1)
draw_circuit(get_mermin_circuits()[0])
