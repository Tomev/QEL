from qiskit import QuantumCircuit, QuantumRegister, transpile, ClassicalRegister
from qiskit.extensions import CnotGate
import sys
sys.path.append('..')
from QEL.Qconfig import APItoken
import numpy as np
from itertools import permutations

basis_gates = ['u1', 'u2', 'u3', 'cx', 'id']
coupling_maps = {
    None: None,
    'T': [[0, 1], [2, 1], [1, 3], [4, 3]],
    'T_bi': [[0, 1], [1, 0], [1, 2], [2, 1], [1, 3], [3, 1], [3, 4], [4, 3]],
    'X': [[0, 1], [1, 2], [0, 2], [3, 2], [3, 4], [4, 2]],
    'X_bi': [[0, 1], [1, 0], [1, 2], [2, 1], [0, 2], [2, 0], [3, 2], [2, 3], [3, 4], [4, 3], [4, 2], [2, 4]],
    'X5': [[0, 1], [1, 0], [1, 2], [2, 1], [2, 3], [3, 2], [3, 0], [0, 3], [3, 4], [4, 3]]
}


def print_transpilations(qc, arch=None, initial_layout=None):
    print("High level circuit:")
    print(qc.draw())
    print(qc.qasm())
    optimals = []
    optimal = None
    layouts = permutations(range(qc.n_qubits)) if initial_layout is None else [initial_layout]
    for layout in layouts:
        for o in range(4):
            qct = transpile(qc, basis_gates=basis_gates, optimization_level=o,
                            coupling_map=coupling_maps[arch], initial_layout=layout)
            n_cx = sum(1 for _ in filter(lambda g: g[0].__class__ == CnotGate, qct.data))
            if optimal is None or n_cx < optimal:
                optimals = [(qct, layout, o)]
                optimal = n_cx
            elif n_cx == optimal:
                optimals.append((qct, layout, o))
    print("Minimal number of cx operations: {0}".format(optimal))
    for (qct, layout, o) in optimals:
        print("Layout: {0}, optimization: {1}, circuit:\n{2}".format(layout, o, qct.draw()))
        print("Source:\n{0}".format(qct.qasm()))


def fourier_circuit(n):
    qr = QuantumRegister(n)
    cr = ClassicalRegister(n)
    qc = QuantumCircuit(qr, cr)
    for i in range(n):
        qc.h(qr[i])
        pw = 1
        for j in range(i + 1, n):
            pw *= 2
            qc.cu1(np.pi / pw, qr[j], qr[i])
    qc.measure(qr, cr)
    return qc


def main():
    print_transpilations(fourier_circuit(4), arch='X')


if __name__ == '__main__':
    main()
