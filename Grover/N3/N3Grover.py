import sys
sys.path.append('../..')
from methods import run_main_loop, test_locally, run_main_loop_with_chsh_test, create_circuit_from_qasm

'''
available_file_names = ['Grover_3_000_2.qasm', 'Grover_3_001_2.qasm', 'Grover_3_010_2.qasm', 'Grover_3_011_2.qasm',
                        'Grover_3_100_2.qasm', 'Grover_3_101_2.qasm', 'Grover_3_110_2.qasm', 'Grover_3_111_2.qasm']

available_file_names = \
    ['Grover-simplified_3_000_2.qasm', 'Grover-simplified_3_001_2.qasm', 'Grover-simplified_3_010_2.qasm',
     'Grover-simplified_3_011_2.qasm', 'Grover-simplified_3_100_2.qasm', 'Grover-simplified_3_101_2.qasm',
     'Grover-simplified_3_110_2.qasm', 'Grover-simplified_3_111_2.qasm']

'''
available_file_names = ['Grover_3_000_1.qasm', 'Grover_3_001_1.qasm', 'Grover_3_010_1.qasm', 'Grover_3_011_1.qasm',
                        'Grover_3_100_1.qasm', 'Grover_3_101_1.qasm', 'Grover_3_110_1.qasm', 'Grover_3_111_1.qasm']

circuits = []

for name in available_file_names:
    qc = create_circuit_from_qasm(name)
    qc.name = name.split('.')[0]
    circuits.append(qc)

run_main_loop_with_chsh_test(circuits)
#test_locally(circuits)
