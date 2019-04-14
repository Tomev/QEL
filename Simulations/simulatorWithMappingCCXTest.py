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


qr = QuantumRegister(5)
cr = ClassicalRegister(5)

print("Simulator with mapping - Reduced Toffoli 3 Test")
print("Selected backend: " + consts.CONSIDERED_REMOTE_BACKENDS[0])

# Create all pairs of cnots
circuits = []

for i in range(5):
    for j in range(5):
        for k in range(5):

            # Continue if there aren't 3 different indices.
            indices = set()
            indices.add(i)
            indices.add(j)
            indices.add(k)

            if len(indices) != 3:
                continue

            circuit = QuantumCircuit(qr, cr)

            # Create state 11111 so that effect is visible.
            circuit.x(qr[0])
            circuit.x(qr[1])
            circuit.x(qr[2])
            circuit.x(qr[3])
            circuit.x(qr[4])

            circuit_name = "Control1: " + str(i) + ", Control2: " + str(j) + ", Target: " + str(k)
            #print(circuit_name)
            circuit += rtof3(i, j, k)
            circuit.name = circuit_name

            circuit.measure(qr, cr)
            circuits.append(circuit)


print("Created " + str(len(circuits)) + " circuits.")

test_locally(circuits, True)
