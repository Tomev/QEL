import numpy as np
import qiskit

from ..methods import run_main_loop, test_locally

# Create a Quantum Register called "qr" with 2 qubits.
qr = qiskit.QuantumRegister(3)
# Create a Classical Register called "cr" with 2 bits.
cr = qiskit.ClassicalRegister(3)


# Prepare a state rotated by theta on the qubit 0.
def prepare_state(t):
    circuit = qiskit.QuantumCircuit(qr, cr)
    circuit.ry(t, qr[0])
    return circuit


# A circuit to measure i-th qubit to i-th bit.
def measure(i):
    circuit = qiskit.QuantumCircuit(qr, cr)
    circuit.measure(qr[i], cr[i])
    return circuit


def get_teleportation_circuits():
    # A circuit to teleport state from qubit 0 to qubit 2.
    teleport = qiskit.QuantumCircuit(qr, cr)

    # Prepare bell state on qubits 1 and 2.
    teleport.h(qr[1])
    teleport.cx(qr[1], qr[2])

    teleport.measure(qr[0], cr[0])
    teleport.measure(qr[1], cr[1])

    # Prepare circuits
    circuits = []

    for theta in np.linspace(0, np.pi, 10):
        qc_test = prepare_state(theta) + measure(0) + measure(1) + measure(2)
        circuits.append(qc_test)
        qc_teleport = prepare_state(theta) + teleport + measure(2)
        circuits.append(qc_teleport)

    return circuits


# Execute
test_locally(get_teleportation_circuits())
