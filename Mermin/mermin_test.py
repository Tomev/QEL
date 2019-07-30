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

    bghz3 = QuantumCircuit(q3, c3)
    bghz3.h(q3[0])
    bghz3.cx(q3[0], q3[1])
    bghz3.cx(q3[0], q3[2])
    bghz3.barrier()

    # quantum circuit to measure XXX
    measure_xxx = QuantumCircuit(q3, c3)
    measure_xxx.h(q3[0])
    measure_xxx.h(q3[1])
    measure_xxx.h(q3[2])
    measure_xxx.measure(q3[0], c3[0])
    measure_xxx.measure(q3[1], c3[1])
    measure_xxx.measure(q3[2], c3[2])

    ghz_xxx = ghz3 + measure_xxx
    ghz_xxx.name = "Mermin_XXX"

    bghz_xxx = bghz3 + measure_xxx
    bghz_xxx.name = "Mermin_XXX_B"

    # Quantum circuit to measure XYY
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
    ghz_xyy.name = "Mermin_XYY"

    bghz_xyy = bghz3 + measure_xyy
    bghz_xyy.name = "Mermin_XYY_B"

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
    ghz_yxy.name = "Mermin_YXY"

    bghz_yxy = bghz3 + measure_yxy
    bghz_yxy.name = "Mermin_YXY_B"

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
    ghz_yyx.name = "Mermin_YYX"

    bghz_yyx = bghz3 + measure_yyx
    bghz_yyx.name = "Mermin_YYX_B"

    circuits = [ghz_xxx, ghz_yyx, ghz_yxy, ghz_xyy, bghz_xxx, bghz_yyx, bghz_yxy, bghz_xyy, ]

    return circuits

run_main_loop_with_chsh_test(get_mermin_circuits())
#test_locally(get_mermin_circuits(), use_mapping=True, save_to_file=True, number_of_simulations=100)
