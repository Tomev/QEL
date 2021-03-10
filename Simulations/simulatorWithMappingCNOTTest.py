from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

from .. import consts
from ..methods import test_locally_with_noise, run_main_loop_with_chsh_test, test_locally

qr = QuantumRegister(5)
cr = ClassicalRegister(5)

print("Simulator with mapping - CNOT Test")
print("Selected backend: " + consts.CONSIDERED_REMOTE_BACKENDS[0])

# Create all pairs of cnots
circuits = []

for i in range(5):
    for j in range(5):

        # Continue if operation would be on one qubit.
        if i == j:
            continue

        circuit = QuantumCircuit(qr, cr)

        # Create state 11111 so that effect is visible.
        circuit.x(qr[0])
        circuit.x(qr[1])
        circuit.x(qr[2])
        circuit.x(qr[3])
        circuit.x(qr[4])

        circuit_name = "Control: " + str(i) + ", Target: " + str(j)
        # print(circuit_name)
        circuit.name = circuit_name
        circuit.cx(qr[i], qr[j])
        circuit.measure(qr, cr)
        circuits.append(circuit)

print("Created " + str(len(circuits)) + " circuits.")

test_locally(circuits)
# test_locally_with_noise(circuits, True)
# run_main_loop_with_chsh_test(circuits)
