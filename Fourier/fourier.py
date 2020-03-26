from qiskit import QuantumCircuit, QuantumRegister, transpile, ClassicalRegister
from qiskit.extensions import CnotGate
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


def n_cnots(circuit):
    return sum(1 for g in circuit.data if isinstance(g[0], CnotGate))


def get_transpilations(qc, arch=None, initial_layout=None):
    optimals = []
    optimal = None
    layouts = permutations(range(qc.n_qubits)) if initial_layout is None else [initial_layout]
    for layout in layouts:
        for o in range(4):
            qct = transpile(qc, basis_gates=basis_gates, optimization_level=o,
                            coupling_map=coupling_maps[arch], initial_layout=layout)
            n_cx = n_cnots(qct)
            if optimal is None or n_cx < optimal:
                optimals = [(qct, layout, o)]
                optimal = n_cx
            elif n_cx == optimal:
                optimals.append((qct, layout, o))

    return optimals


def fourier_circuit(n, measure=True, regs=None):
    """
    regs must be a list(Register) or None. If regs is not None the total number of qubits in the registers in regs
    has to exceed n; first n qubits from the registers will be used for the transform. If measure is True, the same
    holds for classical bits
    """
    if regs is None:
        qc = QuantumCircuit(n, n)
    elif all((isinstance(reg, QuantumRegister) or isinstance(reg, ClassicalRegister) for reg in regs)):
        qc = QuantumCircuit(*regs)
        if len(qc.qubits) < n:
            raise ValueError("Too few qubits in the registers")
        if measure and len(qc.clbits) < n:
            raise ValueError("Too few classical bits in the registers")
    else:
        raise ValueError("Invalid registers")

    for i in range(n):
        qc.h(i)
        pw = 1
        for j in range(i + 1, n):
            pw *= 2
            qc.cu1(np.pi / pw, j, i)
    if measure:
        qc.measure(range(n), range(n))
    return qc


def main():
    qc = fourier_circuit(4)

    print("High level circuit:")
    print(qc.draw())
    print(qc.qasm())

    optimals = get_transpilations(qc, arch='X')

    print("Minimal number of cx operations: {0}".format(n_cnots(optimals[0][0])))

    for (qct, layout, o) in optimals:
        print("Layout: {0}, optimization: {1}, circuit:\n{2}".format(layout, o, qct.draw()))
        print("Source:\n{0}".format(qct.qasm()))


if __name__ == '__main__':
    main()
