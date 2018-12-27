import sys
sys.path.append('../..')
from methods import run_main_loop, test_locally, run_main_loop_with_chsh_test, create_circuit_from_qasm

available_file_names = ['Grover_N3_000.qasm', 'Grover_N3_001.qasm', 'Grover_N3_010.qasm', 'Grover_N3_011.qasm',
                        'Grover_N3_100.qasm', 'Grover_N3_101.qasm', 'Grover_N3_110.qasm', 'Grover_N3_111.qasm']

available_simplified_file_names = \
    ['Grover_N3_000_simplified.qasm', 'Grover_N3_001_simplified.qasm', 'Grover_N3_010_simplified.qasm',
     'Grover_N3_011_simplified.qasm', 'Grover_N3_100_simplified.qasm', 'Grover_N3_101_simplified.qasm',
     'Grover_N3_110_simplified.qasm', 'Grover_N3_111_simplified.qasm']

selected_file_index = 0

circuits = []

for name in available_file_names:
    qc = create_circuit_from_qasm(name)
    qc.name = name
    circuits.append(qc)

run_main_loop_with_chsh_test(circuits)
#run_main_loop(circuits)
#test_locally(circuits)
