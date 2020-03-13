import sys
sys.path.append('../..')
from Fourier.fourier import fourier_circuit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.extensions import U1Gate
import numpy as np


gate = U1Gate(np.pi)


def phase_estimation_circuit(num_approximation_bits, gate, min_success_probability=None):
    if min_success_probability is not None:
        num_approximation_qubits = num_approximation_bits +\
                                   int(np.ceil(np.log2(2 + 1 / (2 * (1 - min_success_probability)))))
    else:
        num_approximation_qubits = num_approximation_bits

    n = num_approximation_qubits + gate.num_qubits
    qr = QuantumRegister(n)
    cr = ClassicalRegister(num_approximation_bits)
    qc = QuantumCircuit(qr, cr)

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

    qc.measure(range(num_approximation_bits), range(num_approximation_bits))

    return qc


def main():
    print(phase_estimation_circuit(3, gate, min_success_probability=0.5))


if __name__ == '__main__':
    main()
