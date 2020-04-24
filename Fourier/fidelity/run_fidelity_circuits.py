import sys
sys.path.append('../..')
from qiskit import IBMQ, QuantumCircuit
from methods import run_main_loop, test_locally, test_locally_with_noise
from Fourier.fourier import fourier_circuit as fc,  get_transpilations
from Fourier.phase_estimation.phase_estimation import phase_estimation_circuit
from qiskit.extensions import U1Gate
import numpy as np


def prepend_x(circuit, qubit):
    circuit.x(qubit)
    circuit.data = circuit.data[-1:] + circuit.data[:-1]


def get_logical_to_physical(qc, n):
    ltp = [None] * n
    for i in range(5):
        if qc._layout[i].register.name != 'ancilla':
            ltp[qc._layout[i].index] = i
    return ltp


def get_circuits(n, arch, backend_name, initial_layout=None):
    # fourier_circuit = QuantumCircuit.from_qasm_file('../circuits/{}'.format(circuit_name))
    # logical_to_physical = [2, 0, 1, 3]
    fourier_circuit = fc(n)
    fourier_circuit = get_transpilations(fourier_circuit, arch=arch, backend_name=backend_name,
                                         initial_layout=initial_layout)[-1][0]
    logical_to_physical = get_logical_to_physical(fourier_circuit, n)
    fourier_circuit.data = fourier_circuit.data[:-(n + 1)]
    inverted_fourier_circuit = fourier_circuit.inverse()
    fourier_circuit.barrier()
    fidelity_circuit = fourier_circuit.extend(inverted_fourier_circuit)
    fidelity_circuit.measure(logical_to_physical, range(n))

    circuits = []

    for state in range(2 ** n):
        circuit = fidelity_circuit.copy()
        for i in range(n):
            if state & (1 << i):
                prepend_x(circuit, logical_to_physical[i])
        circuits.append(circuit)

    return circuits, logical_to_physical


def main():
    n = 3
    # n = 4
    # circuit_name = 'F4X.txt'
    arch = 'T'
    backend_name = 'ibmq_london'
    logical_to_physical = [1, 3, 4]

    circuits, logical_to_physical = get_circuits(n, arch, backend_name, initial_layout=logical_to_physical)

    job_base_name = "F{}{}_fid_comp_base".format(n, arch)

    # job_name_format = "{{}}_{{:0{}b}}".format(n)
    # for state in range(2 ** n):
    #     run_main_loop([circuits[state]], job_name=job_name_format.format(job_base_name, state))

    run_main_loop(circuits, job_name="{}_ltp={}_all".format(job_base_name, logical_to_physical))

    # test_locally(circuits)

    # test_locally_with_noise(circuits)


if __name__ == '__main__':
    main()
