import sys
sys.path.append('../..')
from Fourier.fourier import fourier_circuit, get_transpilations
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.extensions import U1Gate
import numpy as np


u1_gate = U1Gate(2 * np.pi * (1 / 2 + 1 / 8 + 1 / 16))


def phase_estimation_circuit(num_approximation_bits, gate, initial_amplitudes=None):
    return phase_estimation_iteration_circuit(range(num_approximation_bits), gate,
                                              initial_amplitudes=initial_amplitudes)


def phase_estimation_iteration_circuit(estimated_bits, gate, less_significant_bits=None, initial_amplitudes=None):
    n_estimated_bits = len(estimated_bits)
    n = n_estimated_bits + gate.num_qubits
    qr = QuantumRegister(n)
    cr = ClassicalRegister(n_estimated_bits)
    qc = QuantumCircuit(qr, cr)

    if initial_amplitudes is not None:
        for qubits, amplitudes in initial_amplitudes:
            qc.initialize(amplitudes, [qr[n_estimated_bits + idx] for idx in qubits])

    for i in range(n_estimated_bits):
        qc.h(qr[i])

    for i, bit in enumerate(estimated_bits):
        cgate = gate.power(1 << bit).control()
        qc.append(cgate, [qr[i]] + qr[-gate.num_qubits:])

    if less_significant_bits:
        # convert a list of bits to a number
        less_significant_phase = int(''.join(map(str, less_significant_bits)), 2) / (1 << len(less_significant_bits))
        for i in range(n_estimated_bits):
            qc.u1(- np.pi * less_significant_phase / (1 << (n_estimated_bits - 1 - i)), qr[i])

    inv_fourier_circuit = fourier_circuit(n_estimated_bits, regs=[qr, cr], measure=False)
    inv_fourier_circuit = inv_fourier_circuit.inverse()
    qc.extend(inv_fourier_circuit)

    qc.measure(qr[:n_estimated_bits], cr)

    return qc


def estimate_phase_iteratively(num_approximation_bits, gate, job_function, initial_amplitudes=None,
                               min_success_probability=None, t=1):
    if min_success_probability is not None:
        num_estimated_bits = num_approximation_bits + int(np.ceil(np.log2(2 + 1 / (2 * (1 - min_success_probability)))))
    else:
        num_estimated_bits = num_approximation_bits

    estimated_bits = []

    current_bit_idx = num_estimated_bits
    while current_bit_idx > 0:
        current_estimated_bit_numbers = range(max(current_bit_idx - t, 0), current_bit_idx)

        circuit = phase_estimation_iteration_circuit(current_estimated_bit_numbers, gate,
                                                     less_significant_bits=estimated_bits,
                                                     initial_amplitudes=initial_amplitudes)
        circuit = get_transpilations(circuit, arch='T')[0][0]

        job = job_function(circuit)
        result = job.result()

        current_estimated_bits_str = max(result.get_counts(), key=result.get_counts().get)
        current_estimated_bits = [int(bit) for bit in reversed(current_estimated_bits_str)]
        estimated_bits = current_estimated_bits + estimated_bits

        current_bit_idx -= t

    return estimated_bits[:num_approximation_bits]


def main():
    # circuit = phase_estimation_circuit(3, u1_gate, initial_amplitudes=[([0], [0, 1])])
    # get_transpilations(circuit, arch='T')

    # from methods import test_locally
    # print(QuantumCircuit.from_qasm_file('../circuits/P3T_1.txt'))

    # from methods import test_locally
    # print(estimate_phase_iteratively(4, u1_gate, lambda circuit: test_locally([circuit])[0],
    #                                  initial_amplitudes=[([0], [0, 1])], t=2))

    from methods import run_main_loop
    print(estimate_phase_iteratively(4, u1_gate, lambda circuit: run_main_loop([circuit])[0],
                                     initial_amplitudes=[([0], [0, 1])], t=2))


if __name__ == '__main__':
    main()
