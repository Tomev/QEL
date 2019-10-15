import numpy as np
import sys
sys.path.append('..')
from methods import test_locally, run_main_loop, test_locally_with_noise, run_main_loop_with_chsh_test, add_measure_in_base
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


qr2 = QuantumRegister(2)
cr2 = ClassicalRegister(2)
qr3 = QuantumRegister(3)
cr3 = ClassicalRegister(3)

bases_N2 = ['ZZ', 'ZX', 'XX', 'XZ']
bases_N3 = {'XXX', 'YYX', 'YXY', 'XYY'}


c1 = QuantumCircuit(qr2, cr2)
c1.name = "SC_00"
c1.measure(qr2, cr2)

c2 = QuantumCircuit(qr2, cr2)
c2.x(qr2[0])
c2.x(qr2[1])
c2.name = "SC_11"
c2.measure(qr2, cr2)

c3 = QuantumCircuit(qr2, cr2)
c3.x(qr2[0])
c3.x(qr2[1])
c3.barrier()
c3.name = "SC_11_B"
c3.measure(qr2, cr2)

c4 = QuantumCircuit(qr3, cr3)
c4.name = "SC_000"
c4.measure(qr3, cr3)

c5 = QuantumCircuit(qr3, cr3)
c5.x(qr3[0])
c5.x(qr3[1])
c5.x(qr3[2])
c5.name = "SC_111"
c5.measure(qr3, cr3)

c6 = QuantumCircuit(qr3, cr3)
c6.x(qr3[0])
c6.x(qr3[1])
c6.x(qr3[2])
c6.name = "SC_111_B"
c6.measure(qr3, cr3)

circuits_2d = [c1, c2, c3]
circuits_3d = [c4, c5, c6]

SC_Circuits = []

for c in circuits_2d:
    for b in bases_N2:
        SC_Circuits.append(add_measure_in_base(c.copy(), b))

for c in circuits_3d:
    for b in bases_N3:
        SC_Circuits.append(add_measure_in_base(c.copy(), b))

run_main_loop_with_chsh_test(SC_Circuits)
#test_locally(SC_Circuits, use_mapping=True, save_to_file=True, number_of_simulations=100)
#test_locally_with_noise(SC_Circuits)
