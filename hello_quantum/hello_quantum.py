"""
Example used in the README. In this example a Bell state is made.
Note: if you have only cloned the QISKit repository but not
used `pip install`, the examples only work from the root directory.
"""

from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit, QISKitError
import time

import methods
from methods import consts


# Create a Quantum Register called "qr" with 2 qubits.
qr = QuantumRegister(2)
# Create a Classical Register called "cr" with 2 bits.
cr = ClassicalRegister(2)
# Create a Quantum Circuit called involving "qr" and "cr"
qc = QuantumCircuit(qr, cr)

# Add a H gate on qubit 0, putting this qubit in superposition.
qc.h(qr[0])
# Add a CX (CNOT) gate on control qubit 0 and target qubit 1, putting
# the qubits in a Bell state.
qc.cx(qr[0], qr[1])
# Add X Pauli gat, to get different Bell state
qc.x(qr[1])
# Barrier added due to qasm parsing issue
# https://github.com/QISKit/qiskit-sdk-py/issues/309
qc.barrier(qr)
# Add a Measure gate to see the state.
qc.measure(qr, cr)

print('Circuit prepared for execution.')

current_backend_index = 0

for iteration_number in range(0, consts.ITERATIONS_NUMBER):

    print('Iteration number: ', iteration_number)

    current_credits_number = methods.get_current_credits()

    # In case there are to little credits
    while current_credits_number < 3:
        print("Current credits number is", current_credits_number,
              'which is less than 3. Waiting 10 minutes to continue.')
        time.sleep(600)
        current_credits_number = methods.get_current_credits()

    print('Getting available backends...')
    available_backends = methods.get_available_remote_backends_names()

    # Actual execution call
    # IMPORTANT https://github.com/QISKit/qiskit-sdk-py/issues/247
    if __name__ == '__main__':
        try:
            backend = methods.get_backend_name_from_number(current_backend_index)

            while not available_backends.__contains__(backend):
                print(backend, ': Currently not available.')
                current_backend_index = (current_backend_index + 1) % len(consts.CONSIDERED_REMOTE_BACKENDS)
                backend = methods.get_backend_name_from_number(current_backend_index)
                print('Trying another backend: ', backend)
                # sleep for 5 secs in case no backends are available
                time.sleep(5)
                # refresh available backends list
                available_backends = methods.get_available_remote_backends_names()

            print("Executing quantum program on backend:", backend)
            methods.execute(qc, backend)

            print("Program send for execution to ", backend, '.')
            current_backend_index = (current_backend_index + 1) % len(consts.CONSIDERED_REMOTE_BACKENDS)

        except QISKitError as ex:
            print('There was an error in the circuit!. Error = {}'.format(ex))
