import sys

dir_path = "D:\\Coding\\Python\\QE\\QREM\\"
sys.path.append(dir_path)
sys.path.append("D:\\Coding\\Python\\QE\\")
print(f"Appended to path: {dir_path}")

print(sys.path)

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
import QREM.povmtools
from QREM.quantum_tomography_qiskit import detector_tomography_circuits
from methods import run_main_loop

# What I want to do now, is prepare POVM for simulated backend. According to our other notebook, I prepare
# calibration circuits first.

qdt_qubit_indices = [0, 1]
qdt_probe_kets = QREM.povmtools.pauli_probe_eigenkets
qdt_calibration_circuits = detector_tomography_circuits(qdt_qubit_indices, qdt_probe_kets)

# Generate additional circuits. Ones from the tutorial.
qr = QuantumRegister(2, 'qreg')
cr = ClassicalRegister(2, 'creg')
qc = QuantumCircuit(qr, cr)

qc.h(qr[0])
qc.h(qr[1])
qc.measure(qr, cr)

qc.name = "hh"

qr2 = QuantumRegister(2, 'qreg2')
cr2 = ClassicalRegister(2, 'creg2')
qc2 = QuantumCircuit(qr2, cr2)

qc2.x(qr2[0])
qc2.cx(qr2[0], qr2[1])
qc2.measure(qr2, cr2)

qc2.name = "xcx"

qr3 = QuantumRegister(2, 'qreg3')
cr3 = ClassicalRegister(2, 'creg3')
qc3 = QuantumCircuit(qr3, cr3)

qc3.h(qr3[0])
qc3.cx(qr3[0], qr3[1])
qc3.measure(qr3, cr3)

qc3.name = "hcx"

test_circuits = qdt_calibration_circuits
test_circuits.append(qc)
test_circuits.append(qc2)
test_circuits.append(qc3)

run_main_loop(test_circuits)
