import numpy as np
import sys

sys.path.append('..')
from methods import test_locally, run_main_loop, test_locally_with_noise, run_main_loop_with_chsh_test, \
    add_measure_in_base
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def get_sc_n2_circuits():
    qr2 = QuantumRegister(2)
    cr2 = ClassicalRegister(2)

    bases_n2 = ['XX', 'YY', 'YX', 'XY']

    # 00 State
    c1 = QuantumCircuit(qr2, cr2)
    c1.name = "SC_00"

    # 11 B State
    c2 = QuantumCircuit(qr2, cr2)
    c2.x(qr2[0])
    c2.x(qr2[1])
    c2.barrier()
    c2.name = "SC_11_B"

    circuits_n2 = [c1, c2]

    sc_n2_circuits = []

    for c in circuits_n2:
        for b in bases_n2:
            sc_n2_circuits.append(add_measure_in_base(c.copy(), b))

    return sc_n2_circuits


def get_sc_n3_circuits():
    qr3 = QuantumRegister(3)
    cr3 = ClassicalRegister(3)

    # bases_n3 = ['XXX', 'YYX', 'YXY', 'XYY', 'ZZX', 'ZXZ', 'XZZ']
    bases_n3 = ['XXX', 'YYX', 'YXY', 'XYY']

    c3 = QuantumCircuit(qr3, cr3)
    c3.name = "SC_000"

    c4 = QuantumCircuit(qr3, cr3)
    c4.x(qr3[0])
    c4.x(qr3[1])
    c4.x(qr3[2])
    c4.barrier()
    c4.name = "SC_111_B"

    circuits_n3 = [c3, c4]

    sc_n3_circuits = []

    for c in circuits_n3:
        for b in bases_n3:
            sc_n3_circuits.append(add_measure_in_base(c.copy(), b))

    return sc_n3_circuits


# run_main_loop_with_chsh_test(get_sc_circuits())
# test_locally(SC_Circuits, use_mapping=True, save_to_file=True, number_of_simulations=100)
# test_locally_with_noise(SC_Circuits)
