from qiskit import load_qasm_file
from methods import run_main_loop

available_file_names = ['Grover_N_2_A_00.qasm', 'Grover_N_2_A_01.qasm', 'Grover_N_2_A_10.qasm', 'Grover_N_2_A_11.qasm']
selected_file_index = 0

circuit = load_qasm_file(available_file_names[selected_file_index], 'GroverN2')

run_main_loop(circuit)





