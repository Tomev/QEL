import qiskit
import sys
sys.path.append('../..')
from methods import run_main_loop, test_locally

available_file_names = ['Grover_N3_000.qasm', 'Grover_N3_001.qasm', 'Grover_N3_010.qasm', 'Grover_N3_011.qasm',
                        'Grover_N3_100.qasm', 'Grover_N3_101.qasm', 'Grover_N3_110.qasm', 'Grover_N3_111.qasm']

available_simplified_file_names = \
    ['Grover_N3_000_simplified.qasm', 'Grover_N3_001_simplified.qasm', 'Grover_N3_010_simplified.qasm',
     'Grover_N3_011_simplified.qasm', 'Grover_N3_100_simplified.qasm', 'Grover_N3_101_simplified.qasm',
     'Grover_N3_110_simplified.qasm', 'Grover_N3_111_simplified.qasm']

selected_file_index = 0

circuits = []

circuits.append(qiskit.load_qasm_file(available_file_names[selected_file_index],
                                      available_file_names[selected_file_index]))
circuits.append(qiskit.load_qasm_file(available_simplified_file_names[selected_file_index],
                                      available_simplified_file_names[selected_file_index]))

run_main_loop(circuits)
#test_locally(circuits)
