import qiskit
from methods import run_main_loop

# available_file_names = ['Grover_N3_000.qasm', 'Grover_N3_001.qasm', 'Grover_N3_010.qasm', 'Grover_N3_011.qasm',
#                        'Grover_N3_100.qasm', 'Grover_N3_101.qasm', 'Grover_N3_110.qasm', 'Grover_N3_111.qasm']

available_file_names = ['Grover_N3_000_optimal.qasm', 'Grover_N3_001_optimal.qasm', 'Grover_N3_010_optimal.qasm',
                        'Grover_N3_011_optimal.qasm', 'Grover_N3_100_optimal.qasm', 'Grover_N3_101_optimal.qasm',
                        'Grover_N3_110_optimal.qasm', 'Grover_N3_111_optimal.qasm']

selected_file_index = 5
circuit = qiskit.load_qasm_file(available_file_names[selected_file_index], 'GroverN3')

run_main_loop(circuit)





