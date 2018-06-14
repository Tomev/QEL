import methods
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

# Creating registers
q = QuantumRegister(2)
c = ClassicalRegister(2)

# quantum circuit to make an entangled bell state
bell = QuantumCircuit(q, c)
bell.h(q[0])
bell.cx(q[0], q[1])

# quantum circuit to measure q in the standard basis
measureZZ = QuantumCircuit(q, c)
measureZZ.measure(q[0], c[0])
measureZZ.measure(q[1], c[1])
bellZZ = bell+measureZZ

# quantum circuit to measure q in the superposition basis
measureXX = QuantumCircuit(q, c)
measureXX.h(q[0])
measureXX.h(q[1])
measureXX.measure(q[0], c[0])
measureXX.measure(q[1], c[1])
bellXX = bell+measureXX

# quantum circuit to measure ZX
measureZX = QuantumCircuit(q, c)
measureZX.h(q[0])
measureZX.measure(q[0], c[0])
measureZX.measure(q[1], c[1])
bellZX = bell+measureZX

# quantum circuit to measure XZ
measureXZ = QuantumCircuit(q, c)
measureXZ.h(q[1])
measureXZ.measure(q[0], c[0])
measureXZ.measure(q[1], c[1])
bellXZ = bell+measureXZ

circuits = [bellZZ,bellXX,bellZX,bellXZ]

observable_first ={'00': 1, '01': -1, '10': 1, '11': -1}
observable_second ={'00': 1, '01': 1, '10': -1, '11': -1}
observable_correlated ={'00': 1, '01': -1, '10': -1, '11': 1}

CHSH = lambda x : x[0]+x[1]+x[2]-x[3]
measure = [measureZZ, measureZX, measureXX, measureXZ]

real_chsh_circuits = []
real_x = []

real_steps = 10
for step in range(real_steps):
    theta = 2.0*np.pi*step/10
    bell_middle = QuantumCircuit(q,c)
    bell_middle.ry(theta,q[0])
    for m in measure:
        real_chsh_circuits.append(bell+bell_middle+m)
    real_x.append(theta)

job = execute(real_chsh_circuits, backend=device_name, coupling_map=device_coupling, shots=device_shots)
result = job.result()
