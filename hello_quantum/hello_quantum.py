"""
Example used in the README. In this example a Bell state is made.
Note: if you have only cloned the QISKit repository but not
used `pip install`, the examples only work from the root directory.
"""

# Import the QISKit SDK
import qiskit
# Import the IBMQ Experience API
from IBMQuantumExperience import IBMQuantumExperience


def get_backend_name(i):
    i = (i+1) % 3
    if i == 0:
        return 'ibmqx2'
    if i == 1:
        return 'ibmqx4'
    if i == 2:
        return 'ibmqx5'


# IMPORTANT https://github.com/QISKit/qiskit-sdk-py/issues/247
if __name__ == '__main__':
    # Authenticate for access to remote backends

    backend_identificator = 0
    i = 1

    try:
        import Qconfig

        api = IBMQuantumExperience(token=Qconfig.APItoken,
                                   config={'url': Qconfig.config['url']})
        remote_backends = qiskit.backends.discover_remote_backends(api)
    except:
        print("""WARNING: There's no connection with IBMQuantumExperience servers.
                 Have you initialized a Qconfig.py file with your personal token?
                 For now, there's only access to local simulator backends...""")
        remote_backends = {}

    while True:
        local_backends = qiskit.backends.discover_local_backends()

        try:
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


            qp.load_qasm_file(name='bell', qasm_file='QASM.txt')
            print(qp.get_qasm('bell'))

            # Compile and run the Quantum Program on a simulator backend
            print("(Local Backends)")
            for backend in local_backends:
                print(backend)
            sim_result = qp.execute("bell", backend='local_qasm_simulator', shots=1024, seed=1)

            # Show the results
            print("simulation: ", sim_result)
            print(sim_result.get_counts("bell"))

            # Compile and run the Quantum Program on a real device backend
            if remote_backends:
                # see a list of available remote backends
                print("\n(Remote Backends)")
                for backend in remote_backends:
                    backend_status = api.backend_status(backend)
                    print(backend, backend_status)

                ## select least busy available device and execute
                # device_status = [api.backend_status(backend)
                #                 for backend in remote_backends if "simulator" not in backend]
                # best_device = min([x for x in device_status if x['available']==True],
                #                  key=lambda x:x['pending_jobs'])
                # print("Running on current least busy device: ", best_device['backend'])
                # exp_result = qp.execute("bell", backend=best_device['backend'], shots=1024, timeout=300)

                #backend = 'ibmqx4'
                backend = get_backend_name(backend_identificator)
                backend_identificator = (backend_identificator + 1) % 3

                #while True:
                print("Iteration: ", i)
                print("Running on fixed device: ", backend)

                qp.load_qasm_file(name='bell', qasm_file='QASM.txt')
                print(qp.get_qasm('bell'))

                exp_result = qp.execute("bell", backend=backend, shots=1024, timeout=5)
                print("Next iteration")
                i += 1
                # Show the results
                print("experiment: ", exp_result)
                print(exp_result.get_counts("bell"))
                print(exp_result.get_data("bell"))

        except qiskit.QISKitError as ex:
            print('There was an error in the circuit!. Error = {}'.format(ex))


