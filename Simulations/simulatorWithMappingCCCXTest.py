import sys

sys.path.append('..\\')
import consts
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from methods import test_locally


def rtof3(control1, control2, target):
    rtof = QuantumCircuit(qr, cr)
    rtof.h(qr[target])
    rtof.t(qr[target])
    rtof.cx(qr[control2], qr[target])
    rtof.tdg(qr[target])
    rtof.cx(qr[control1], qr[target])
    rtof.t(qr[target])
    rtof.cx(qr[control2], qr[target])
    rtof.tdg(qr[target])
    rtof.h(qr[target])
    return rtof


def rtof4(c1, c2, c3, t):

    a = 2  # ancilla

    rtof = QuantumCircuit(qr, cr)
    rtof += rtof3(c1, c2, a)
    rtof += rtof3(a, c3, t)
    rtof += rtof3(c1, c2, a)

    return rtof


qr = QuantumRegister(5)
cr = ClassicalRegister(5)

print("Simulator with mapping - Reduced Toffoli 4 Test")
print("Selected backend: " + consts.CONSIDERED_REMOTE_BACKENDS[0])

# Create all pairs of cccnots
circuits = []

for i in range(5):
    for j in range(5):
        for k in range(5):
            for l in range(5):

                # Continue if there aren't 4 different indices.
                indices = set()
                indices.add(i)
                indices.add(j)
                indices.add(k)
                indices.add(l)

                if len(indices) != 4:
                    continue

                if indices.__contains__(2):
                    continue  # contains ancilla

                circuit = QuantumCircuit(qr, cr)

                # Create state 11111 so that effect is visible.
                circuit.x(qr[0])
                circuit.x(qr[1])
                #circuit.x(qr[2])
                circuit.x(qr[3])
                circuit.x(qr[4])

                circuit_name = "Control1: " + str(i) + ", Control2: " + str(j) + ", Target: " + str(k)
                #print(circuit_name)
                circuit += rtof4(i, j, k, l)
                circuit.name = circuit_name

                circuit.measure(qr, cr)
                circuits.append(circuit)


print("Created " + str(len(circuits)) + " circuits.")

test_locally(circuits, True)
