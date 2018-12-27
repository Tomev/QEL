import sys
sys.path.append('../..')
from methods import run_main_loop, test_locally, create_circuit_from_qasm, run_main_loop_with_chsh_test

available_file_names = ['Grover_N2_00.qasm', 'Grover_N2_01.qasm', 'Grover_N2_10.qasm', 'Grover_N2_11.qasm']
selected_file_index = 0

circuits = []

for file_name in available_file_names:
    qc = create_circuit_from_qasm(file_name)
    qc.name = file_name
    circuits.append(qc)

run_main_loop_with_chsh_test(circuits)
#test_locally(circuits)
#run_main_loop(circuits)
