"""
Example used in the README. In this example a Bell state is made.
Note: if you have only cloned the QISKit repository but not
used `pip install`, the examples only work from the root directory.
"""

from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit, QISKitError

from methods import run_main_loop


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

# Assign circuits to run here.

run_main_loop(qc)
