import sys
sys.path.append('../..')
from qiskit import IBMQ, QuantumCircuit
from methods import run_main_loop, test_locally, test_locally_with_noise


n = 3
circuit_name = "F3X.txt"
job_base_name = "F3X_fidelity_computational_base"
logical_to_physical = [0, 1, 2]


def prepend_x(circuit, qubit):
    circuit.x(qubit)
    circuit.data = circuit.data[-1:] + circuit.data[:-1]


def get_circuits():
    fourier_circuit = QuantumCircuit.from_qasm_file('../circuits/{}'.format(circuit_name))
    fourier_circuit.data = fourier_circuit.data[:-(n + 1)]
    inverted_fourier_circuit = fourier_circuit.inverse()
    fourier_circuit.barrier()
    fidelity_circuit = fourier_circuit.extend(inverted_fourier_circuit)
    fidelity_circuit.measure(range(n), range(n))

    circuits = []

    for state in range(2 ** n):
        circuit = fidelity_circuit.copy()
        for i in range(n):
            if state & (1 << i):
                prepend_x(circuit, logical_to_physical[i])
        circuits.append(circuit)

    return circuits


def main():
    circuits = get_circuits()

    # job_name_format = "{{}}_{{:0{}b}}".format(n)
    # for state in range(2 ** n):
    #     run_main_loop([circuits[state]], job_name=job_name_format.format(job_base_name, state))

    run_main_loop(circuits, job_name="{}_all".format(job_base_name))

    # test_locally(circuits)

    # test_locally_with_noise(circuits)


if __name__ == '__main__':
    main()
