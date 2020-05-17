import sys
sys.path.append('..')
from qiskit.ignis.mitigation.measurement import complete_meas_cal
from qiskit import transpile, assemble
from methods import get_backend_from_name


def main():
    backend_name = 'ibmq_london'
    num_qubits = 5

    meas_calibs, state_labels = complete_meas_cal(range(num_qubits), circlabel='mcal')

    backend = get_backend_from_name(backend_name)

    experiments = transpile(meas_calibs, backend=backend, optimization_level=3)

    backend.run(assemble(experiments, shots=8192), job_name="mitigation_test_calibration")


if __name__ == '__main__':
    main()
