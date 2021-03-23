import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.append(parent_dir)

from methods import test_locally, create_circuit_from_qasm

available_file_names = ['Grover_3_000_1.qasm']

circuits = []

for name in available_file_names:
    qc = create_circuit_from_qasm(name)
    qc.name = name.split('.')[0]
    circuits.append(qc)

# run_main_loop_with_chsh_test(circuits)
test_locally(circuits)
