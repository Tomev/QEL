import sys
sys.path.append('../..')
from Fourier.fourier import fourier_circuit, print_transpilations
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.extensions import U1Gate
import numpy as np


u1_gate = U1Gate(2 * np.pi * (1 / 2 + 1 / 8))


def phase_estimation_circuit(num_approximation_bits, gate, initial_amplitudes=None, min_success_probability=None):
    if min_success_probability is not None:
        num_approximation_qubits = num_approximation_bits +\
                                   int(np.ceil(np.log2(2 + 1 / (2 * (1 - min_success_probability)))))
    else:
        num_approximation_qubits = num_approximation_bits

    n = num_approximation_qubits + gate.num_qubits
    qr = QuantumRegister(n)
    cr = ClassicalRegister(num_approximation_bits)
    qc = QuantumCircuit(qr, cr)

    if initial_amplitudes is not None:
        for qubits, amplitudes in initial_amplitudes:
            qc.initialize(amplitudes, [qr[idx + num_approximation_qubits] for idx in qubits])

    for i in range(num_approximation_qubits):
        qc.h(qr[i])

    pw = 1
    for i in range(num_approximation_qubits):
        cgate = gate.power(pw).control()
        qc.append(cgate, [qr[i]] + qr[-gate.num_qubits:])
        pw *= 2

    inv_fourier_circuit = fourier_circuit(num_approximation_qubits, regs=[qr, cr], measure=False)
    inv_fourier_circuit = inv_fourier_circuit.inverse()
    qc.extend(inv_fourier_circuit)

    qc.measure(qr[:num_approximation_bits], cr)

    return qc


def phase_estimation_iteration_circuit(estimated_bit, gate, less_significant_bits=None, initial_amplitudes=None):
    n = gate.num_qubits + 1
    qr = QuantumRegister(n)
    cr = ClassicalRegister(1)
    qc = QuantumCircuit(qr, cr)

    if initial_amplitudes is not None:
        for qubits, amplitudes in initial_amplitudes:
            qc.initialize(amplitudes, [qr[idx + 1] for idx in qubits])

    qc.h(qr[0])

    cgate = gate.power(2 ** estimated_bit).control()
    qc.append(cgate, [qr[0]] + [qr[-gate.num_qubits]])

    if less_significant_bits:
        # convert a list of bits to a number
        less_significant_phase = int(''.join(map(str, less_significant_bits)), 2) / (1 << len(less_significant_bits))
        qc.u1(- np.pi * less_significant_phase, qr[0])

    qc.h(qr[0])

    qc.measure(qr[0], cr)

    return qc


def estimate_phase_iteratively(num_approximation_bits, gate, job_function, initial_amplitudes=None,
                               min_success_probability=None):
    if min_success_probability is not None:
        num_estimated_bits = num_approximation_bits + int(np.ceil(np.log2(2 + 1 / (2 * (1 - min_success_probability)))))
    else:
        num_estimated_bits = num_approximation_bits

    estimated_bits = []

    for bit_number in reversed(range(num_estimated_bits)):
        circuit = phase_estimation_iteration_circuit(bit_number, gate, less_significant_bits=estimated_bits,
                                                     initial_amplitudes=initial_amplitudes)
        job = job_function(circuit)
        result = job.result()
        bit = 1 if result.get_counts().get('1', 0) > result.get_counts().get('0', 0) else 0
        estimated_bits.insert(0, bit)

    return estimated_bits[:num_approximation_bits]


def main():
    # circuit = phase_estimation_circuit(3, u1_gate, initial_amplitudes=[([0], [0, 1])])
    # print_transpilations(circuit, arch='T')

    # from methods import test_locally
    # print(QuantumCircuit.from_qasm_file('../circuits/P3T_1.txt'))

    # from methods import test_locally
    # print(estimate_phase_iteratively(3, u1_gate, lambda circuit: test_locally([circuit])[0],
    #                                  initial_amplitudes=[([0], [0, 1])]))

    from methods import run_main_loop
    print(estimate_phase_iteratively(3, u1_gate, lambda circuit: run_main_loop([circuit])[0],
                                     initial_amplitudes=[([0], [0, 1])]))


if __name__ == '__main__':
    main()
