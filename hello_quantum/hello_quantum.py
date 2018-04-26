"""
Example used in the README. In this example a Bell state is made.
Note: if you have only cloned the QISKit repository but not
used `pip install`, the examples only work from the root directory.
"""

import qiskit
from IBMQuantumExperience import IBMQuantumExperience
import os.path
import Qconfig
import time


# Settings
qasm_file_name = 'QASM.txt'
quantum_circuit_name = 'bell'
considered_backends = ['ibmqx2', 'ibmqx4', 'ibmqx5']
iterations_number = 1000000

def get_backend_name_from_number(backend_index):
    backend_index = backend_index % len(considered_backends)
    return considered_backends[backend_index]


def create_qasm_file():
    # Create a Quantum Register called "qr" with 2 qubits.
    qr = qiskit.QuantumRegister("qr", 2)
    # Create a Classical Register called "cr" with 2 bits.
    cr = qiskit.ClassicalRegister("cr", 2)
    # Create a Quantum Circuit called involving "qr" and "cr"
    qc = qiskit.QuantumCircuit(qr, cr)

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

    # Create a Quantum Program for execution
    qp = qiskit.QuantumProgram()
    # Add the circuit you created to it, and call it the "bell" circuit.
    # (You can add multiple circuits to the same program, for batch execution)
    qp.add_circuit("bell", qc)

    qasm_file = open(qasm_file_name, 'w')

    qasm_file.write(qp.get_qasm())

    qasm_file.close()


def get_available_backends():
    api = IBMQuantumExperience(token=Qconfig.APItoken, config={'url': Qconfig.config['url']})
    discovered_backends = qiskit.backends.discover_remote_backends(api)

    if discovered_backends == {}:
        print("""WARNING: There's no connection with IBMQuantumExperience servers.
                 Have you initialized a Qconfig.py file with your personal token?
                 For now, there's only access to local simulator backends...""")
    else:
        # Select only available ones
        for backend_index in range(len(discovered_backends) - 1, 0, -1):
            backend_status = api.backend_status(discovered_backends[backend_index])

            if not backend_status['available']:
                discovered_backends.remove(discovered_backends[backend_index])

    return discovered_backends


current_backend_index = 0
my_api = IBMQuantumExperience(token=Qconfig.APItoken, config={'url': Qconfig.config['url']})

for iteration_number in range(0, iterations_number):

    print('Iteration number: ', iteration_number)

    current_credits_number = my_api.get_my_credits()['remaining']

    # In case there are to little credits
    while current_credits_number < 3:
        print("Current credits number is", current_credits_number,
              'which is less than 3. Waiting 10 minutes to continue.')
        time.sleep(600)
        current_credits_number = my_api.get_my_credits()['remaining']

    # Check if there's a qasm file, if not create it
    if not os.path.exists('.\\'+qasm_file_name):
        print("Creating qasm file of a program...")
        create_qasm_file()

    print('Getting available backends...')
    available_backends = get_available_backends()

    # Actual execution call
    # IMPORTANT https://github.com/QISKit/qiskit-sdk-py/issues/247
    if __name__ == '__main__':
        try:
            qp = qiskit.QuantumProgram()
            print('Loading qasm from file to program...')
            qp.load_qasm_file(name=quantum_circuit_name, qasm_file=qasm_file_name)
            backend = get_backend_name_from_number(current_backend_index)

            while not available_backends.__contains__(backend):
                print(backend, ': Currently not available.')
                current_backend_index = (current_backend_index + 1) % len(considered_backends)
                backend = get_backend_name_from_number(current_backend_index)
                print('Trying another backend: ', backend)
                # sleep for 5 secs in case no backends are available
                time.sleep(5)

            print("Executing quantum program on backend: ", backend)
            qp.execute(quantum_circuit_name, backend=backend, shots=1024, timeout=0)

            print("Program send for execution to ", backend, '.')
            current_backend_index = (current_backend_index + 1) % len(considered_backends)

        except qiskit.QISKitError as ex:
            print('There was an error in the circuit!. Error = {}'.format(ex))
