import sys
sys.path.append('../..')
from qiskit import IBMQ, QuantumCircuit
from methods import run_main_loop, test_locally, test_locally_with_noise


def main():
    fourier_circuit = QuantumCircuit.from_qasm_file('../circuits/F3X.txt')
    fourier_circuit.data = fourier_circuit.data[:-3]
    inverted_fourier_circuit = fourier_circuit.inverse()
    fourier_circuit.barrier()
    fidelity_circuit = fourier_circuit.extend(inverted_fourier_circuit)
    fidelity_circuit.measure(range(3), range(3))

    circuits = []

    for state in range(8):
        circuit = fidelity_circuit.copy()
        for i in range(3):
            if state & (1 << i):
                prepend_x(circuit, i)
        run_main_loop([circuit], job_name="F3X_fidelity_computational_base_{:03b}".format(state))
        circuits.append(circuit)

    # run_main_loop(circuits, job_name="F3X_fidelity_computational_base_all")

    # test_locally(circuits)

    # test_locally_with_noise(circuits)


def prepend_x(circuit, qubit):
    circuit.x(qubit)
    circuit.data = circuit.data[-1:] + circuit.data[:-1]


if __name__ == '__main__':
    main()
