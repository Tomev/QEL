from qiskit import load_qasm_file
from methods import run_main_loop

available_file_names = ['Grover_N3.qasm']
selected_file_index = 0

circuit = load_qasm_file(available_file_names[selected_file_index], 'GroverN3')

run_main_loop(circuit)





