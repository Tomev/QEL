import sys
sys.path.append('../..')
from qiskit import load_qasm_file
from methods import run_main_loop, test_locally

available_file_names = ['Grover_N_2_A_00.qasm', 'Grover_N_2_A_01.qasm', 'Grover_N_2_A_10.qasm', 'Grover_N_2_A_11.qasm']
selected_file_index = 0

circuits = []

for file_name in available_file_names:
    circuits.append(load_qasm_file(file_name, file_name))

#test_locally(circuits)
run_main_loop(circuits)





