import sys
sys.path.append('../..')
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
    circuits = []

    for state in range(2 ** n):
        circuit = phase_estimation_circuit(n, U1Gate(2 * np.pi * state / (2 ** n)), initial_amplitudes=[([0], [0, 1])])
        circuit = get_transpilations(circuit, arch=arch, backend_name=backend_name,
                                     initial_layout=initial_layout)[-1][0]
        circuits.append(circuit)

    return circuits


def main():
    n = 3
    logical_to_physical = [3, 4, 0, 2]
    arch = 'X'
    job_base_name = "pe_fid"
    backend_name = 'ibmqx2'

    circuits = get_circuits(n, arch, backend_name, initial_layout=logical_to_physical)

    # job_name_format = "{{}}_{{:0{}b}}".format(n)
    # for state in range(2 ** n):
    #     run_main_loop([circuits[state]], job_name=job_name_format.format(job_base_name, state))

    run_main_loop(circuits, job_name="{}_ltp={}_all".format(job_base_name, logical_to_physical))

    # test_locally(circuits)

    # test_locally_with_noise(circuits)


if __name__ == '__main__':
    main()
