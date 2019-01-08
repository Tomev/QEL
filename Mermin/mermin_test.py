import sys
sys.path.append('../')

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from methods import run_main_loop_with_chsh_test, test_locally


def get_mermin_circuits():
    # 3 - qubits 
    # quantum circuit to make GHZ state 
    q3 = QuantumRegister(3)
    c3 = ClassicalRegister(3)
    ghz3 = QuantumCircuit(q3, c3)
    ghz3.h(q3[0])
    ghz3.cx(q3[0], q3[1])
    ghz3.cx(q3[0], q3[2])

    # quantum circuit to measure XXX
    measure_xxx = QuantumCircuit(q3, c3)
    measure_xxx.h(q3[0])
    measure_xxx.h(q3[1])
    measure_xxx.h(q3[2])
    measure_xxx.measure(q3[0], c3[0])
    measure_xxx.measure(q3[1], c3[1])
    measure_xxx.measure(q3[2], c3[2])
    ghz_xxx = ghz3 + measure_xxx

    # quantum circuit to measure XYY
    measure_xyy = QuantumCircuit(q3, c3)
    measure_xyy.s(q3[1]).inverse()
    measure_xyy.s(q3[2]).inverse()
    measure_xyy.h(q3[0])
    measure_xyy.h(q3[1])
    measure_xyy.h(q3[2])
    measure_xyy.measure(q3[0], c3[0])
    measure_xyy.measure(q3[1], c3[1])
    measure_xyy.measure(q3[2], c3[2])
    ghz_xyy = ghz3 + measure_xyy

    # quantum circuit to measure q YXY
    measure_yxy = QuantumCircuit(q3, c3)
    measure_yxy.s(q3[0]).inverse()
    measure_yxy.s(q3[2]).inverse()
    measure_yxy.h(q3[0])
    measure_yxy.h(q3[1])
    measure_yxy.h(q3[2])
    measure_yxy.measure(q3[0], c3[0])
    measure_yxy.measure(q3[1], c3[1])
    measure_yxy.measure(q3[2], c3[2])
    ghz_yxy = ghz3 + measure_yxy

    # quantum circuit to measure q YYX
    measure_yyx = QuantumCircuit(q3, c3)
    measure_yyx.s(q3[0]).inverse()
    measure_yyx.s(q3[1]).inverse()
    measure_yyx.h(q3[0])
    measure_yyx.h(q3[1])
    measure_yyx.h(q3[2])
    measure_yyx.measure(q3[0], c3[0])
    measure_yyx.measure(q3[1], c3[1])
    measure_yyx.measure(q3[2], c3[2])
    ghz_yyx = ghz3 + measure_yyx

    circuits = [ghz_xxx, ghz_yyx, ghz_yxy, ghz_xyy]

    return circuits


# run_main_loop_with_chsh_test(get_mermin_circuits())
test_locally(get_mermin_circuits())

