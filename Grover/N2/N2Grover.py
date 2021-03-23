import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.append(parent_dir)

from methods import test_locally, create_circuit_from_qasm

available_file_names = ['Grover_2_00_1.qasm', 'Grover_2_01_1.qasm', 'Grover_2_10_1.qasm', 'Grover_2_11_1.qasm']
selected_file_index = 0

circuits = []

for file_name in available_file_names:
    qc = create_circuit_from_qasm(file_name)
    qc.name = file_name.split('.')[0]
    circuits.append(qc)

# run_main_loop_with_chsh_test(circuits)
test_locally(circuits)
