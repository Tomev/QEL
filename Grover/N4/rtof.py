from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

# Mapowanie
C0 = 3
C1 = 4
C2 = 1
T = 0
A = 2
qubits_indexes_by_occurrence = [C0, C1, C2, T]

qr = QuantumRegister(5)
cr = ClassicalRegister(5)


def rtof3(control1, control2, target):
    rtof = QuantumCircuit(qr, cr)

    rtof.h(qr[target])
    rtof.t(qr[target])
    rtof.cx(qr[control2], qr[target])
    rtof.tdg(qr[target])
    rtof.cx(qr[control1], qr[target])
    rtof.t(qr[target])
    rtof.cx(qr[control2], qr[target])
    rtof.tdg(qr[target])
    rtof.h(qr[target])

    return rtof


def ccnot(control1, control2, target):
    circuit = QuantumCircuit(qr, cr)
    circuit.ccx(qr[control1], qr[control2], qr[target])
    return (circuit)


def rtof4():
    rtof4 = rtof3(C0, C1, A) + ccnot(A, C2, T) + rtof3(C0, C1, A)
    return rtof4

# print(rtof4())
# print()
