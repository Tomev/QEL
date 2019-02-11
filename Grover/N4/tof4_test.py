import qiskit
import sys
import warnings
sys.path.append('../..')
from methods import test_locally, run_main_loop_with_chsh_test


qr = qiskit.QuantumRegister(5)
cr = qiskit.ClassicalRegister(5)


# 2,3,4 - control, 1 - target, 0 - ancillae
def ccnot(control1, control2, target):
    q_circuit = qiskit.QuantumCircuit(qr, cr)
    q_circuit.ccx(qr[control1], qr[control2], qr[target])
    return q_circuit


def rtof3(control1, control2, target):
    rtof = qiskit.QuantumCircuit(qr, cr)
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


def prepare_state(q_state):
    prepare = qiskit.QuantumCircuit(qr, cr)
    for i in range(4):
        if q_state[i] == '1':
            prepare.x(qr[4-i])
    return prepare


def expected_cccnot(q_state):
    if q_state[:3] == '111':
        return '111' + str(int(not(bool(int(q_state[3])))))
    return q_state


rtof4 = rtof3(2, 3, 0) + ccnot(0, 4, 1) + rtof3(2, 3, 0)

states = ['{0:04b}'.format(x) for x in range(2**4)]

warnings.filterwarnings('ignore')

circuits = []

for state in states:
    circuit = prepare_state(state) + rtof4
    circuit.measure(qr, cr)
    circuit.name = str("tof4 " + state + " - expected: " + expected_cccnot(state) + "0")
    circuits.append(circuit)

# test_locally(circuits)
run_main_loop_with_chsh_test(circuits)
