import sys
import warnings
sys.path.append('../..')
from methods import run_main_loop_with_chsh_test, execute_circuits, test_locally
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

qr = QuantumRegister(5)
cr = ClassicalRegister(5)

#Mapowanie
C1 = 3
C2 = 4
C3 = 1
T = 0
A = 2


def ccnot(control1, control2, target):
    quantum_circuit = QuantumCircuit(qr, cr)
    quantum_circuit.ccx(qr[control1], qr[control2], qr[target])
    return quantum_circuit


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


def prepare_state(quantum_state):

    prepared_circuit = QuantumCircuit(qr, cr)

    if quantum_state[0] == '1':
        prepared_circuit.x(qr[C1])
    if quantum_state[1] == '1':
        prepared_circuit.x(qr[C2])
    if quantum_state[2] == '1':
        prepared_circuit.x(qr[C3])
    if quantum_state[3] == '1':
        prepared_circuit.x(qr[T])

    return prepared_circuit


def expected_cccnot(quantum_state):

    if quantum_state == '1110':
        expected = '1111'
    else:
        if (quantum_state == '1111'):
            expected = '1110'
        else:
            expected = quantum_state

    mapped_expected = list('xxxxx')
    mapped_expected[C1] = expected[0]
    mapped_expected[C2] = expected[1]
    mapped_expected[C3] = expected[2]
    mapped_expected[T] = expected[3]
    mapped_expected[A] = '0'
    mapped_expected = list(reversed(mapped_expected))
    mapped_expected = "".join(mapped_expected)

    return mapped_expected


measure_all = QuantumCircuit(qr, cr)
measure_all.measure(qr, cr)

rtof4 = rtof3(C1, C2, A) + ccnot(A, C3, T) + rtof3(C1, C2, A)

states = ['{0:04b}'.format(x) for x in range(2**4)]

"".join(list(reversed(['1', 'x'])))

circuits = []

for state in states:
    circuit = prepare_state(state) + rtof4
    circuit.measure(qr, cr)
    circuit.name = str("tof4 " + state + " - expected: " + expected_cccnot(state))
    circuits.append(circuit)

test_locally(circuits)
# run_main_loop_with_chsh_test(circuits)
