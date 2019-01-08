import sys
sys.path.append('..\\..')

from methods import test_locally, run_main_loop, run_main_loop_with_chsh_test
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from Grover.N4.rtof import rtof4

# Mapowanie
C0 = 3
C1 = 4
C2 = 1
T = 0
A = 2
qubits_indexes_by_occurrence = [C0, C1, C2, T]

qr = QuantumRegister(5)
cr = ClassicalRegister(5)
qc = QuantumCircuit(qr, cr)
algorithm_repetition_times = 3


def rtof3(control1, control2, target):

    global qc

    qc.h(qr[target])
    qc.t(qr[target])
    qc.cx(qr[control2], qr[target])
    qc.tdg(qr[target])
    qc.cx(qr[control1], qr[target])
    qc.t(qr[target])
    qc.cx(qr[control2], qr[target])
    qc.tdg(qr[target])
    qc.h(qr[target])


def ccnot(control1, control2, target):
    global qc
    qc.ccx(qr[control1], qr[control2], qr[target])


def rtof4():
    global qc
    rtof3(C0, C1, A)
    ccnot(A, C2, T)
    rtof3(C0, C1, A)


def initialization(selected_state):

    global qc
    global qr
    global cr
    global algorithm_repetition_times

    circuit_name = 'Grover_4_' + str(selected_state) + '_' + str(algorithm_repetition_times)

    qr = QuantumRegister(5)
    cr = ClassicalRegister(5)
    qc = QuantumCircuit(qr, cr, name=circuit_name)

    qc.h(qr[C0])
    qc.h(qr[C1])
    qc.h(qr[C2])
    qc.h(qr[T])


def oracle(selected_state):

    global qubits_indexes_by_occurrence
    global qc

    xs_positions = []

    for j in range(len(selected_state)):
        if selected_state[j] == '0':
            xs_positions.append(qubits_indexes_by_occurrence[j])

    for pos in xs_positions:
        qc.x(qr[pos])

    qc.h(qr[T])
    rtof4()
    qc.h(qr[T])

    for pos in xs_positions:
        qc.x(qr[pos])


def diffusion():
    global qc

    qc.h(qr[C0])
    qc.h(qr[C1])
    qc.h(qr[C2])
    qc.h(qr[T])

    qc.x(qr[C0])
    qc.x(qr[C1])
    qc.x(qr[C2])
    qc.x(qr[T])

    qc.h(qr[T])
    rtof4()
    qc.h(qr[T])

    qc.x(qr[C0])
    qc.x(qr[C1])
    qc.x(qr[C2])
    qc.x(qr[T])

    qc.h(qr[C0])
    qc.h(qr[C1])
    qc.h(qr[C2])
    qc.h(qr[T])


states = ['{0:04b}'.format(x) for x in range(2**4)]
circuits = []


for state in states:
    initialization(state)

    for i in range(algorithm_repetition_times):
        oracle(state)
        diffusion()

    qc.measure(qr, cr)
    circuits.append(qc)

test_locally(circuits)
#run_main_loop_with_chsh_test(circuits)
