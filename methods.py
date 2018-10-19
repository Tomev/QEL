from qiskit import execute, IBMQ, Aer
from IBMQuantumExperience import IBMQuantumExperience
import qiskit
import time

import Qconfig
import consts


def get_operational_remote_backends():
    operational_backends = IBMQ.backends(operational=True, filters=lambda x: not x.configuration()['simulator'])
    return operational_backends


def get_backends_names(backends):
    names = []

    for backend in backends:
        names.append(backend.name())

    return names


def get_backend_from_name(name):
    return IBMQ.get_backend(name)


def get_sim_backend_from_name(name):
    return Aer.get_backend(name)


def get_current_credits():
    api = IBMQuantumExperience(token=Qconfig.APItoken, config=Qconfig.config)
    return api.get_my_credits()['remaining']


def get_backend_name_from_number(backend_index):
    backend_index = backend_index % len(consts.CONSIDERED_REMOTE_BACKENDS)
    return consts.CONSIDERED_REMOTE_BACKENDS[backend_index]


def execute_circuits(circuits, backend):
    return execute(circuits, backend, shots=consts.SHOTS)


def run_main_loop(circuits):
    current_backend_index = 0
    wait_time_in_minutes = 5

    for iteration_number in range(0, consts.ITERATIONS_NUMBER):

        print('Iteration number: ', iteration_number)

        current_credits_number = get_current_credits()

        # In case there are to little credits
        while current_credits_number < 3:
            print("Current credits number is", current_credits_number,
                  'which is less than 3. Waiting ' + str(wait_time_in_minutes) + ' minute(s) to continue.')
            time.sleep(wait_time_in_minutes * 60)
            current_credits_number = get_current_credits()

        print('Getting available backends...')
        operational_remote_backends = get_operational_remote_backends()

        # Actual execution call
        # IMPORTANT https://github.com/QISKit/qiskit-sdk-py/issues/247
        # if __name__ == '__main__':
        try:
            backend_name = get_backend_name_from_number(current_backend_index)
            operational_remote_backends_names = get_backends_names(operational_remote_backends)

            while not operational_remote_backends_names.__contains__(backend_name):
                print(backend_name, ': Currently not available.')
                print("Operational backends:")
                print(operational_remote_backends_names)
                current_backend_index = (current_backend_index + 1) % len(consts.CONSIDERED_REMOTE_BACKENDS)
                backend_name = get_backend_name_from_number(current_backend_index)
                print('Refreshing available backends list...')
                operational_remote_backends = get_operational_remote_backends()
                operational_remote_backends_names = get_backends_names(operational_remote_backends)
                print('Trying backend %s. ' % backend_name)

            print("Executing quantum program on %s." % backend_name)
            execute_circuits(circuits, get_backend_from_name(backend_name))

            print("Program sent for execution to ", backend_name, '.')
            current_backend_index = (current_backend_index + 1) % len(consts.CONSIDERED_REMOTE_BACKENDS)

        except qiskit.QISKitError as ex:
            print('There was an error in the circuit!. Error = {}'.format(ex))


def test_locally(circuit):
    backend = get_sim_backend_from_name("qasm_simulator")
    executed_job = execute_circuits(circuit, backend)
    print(executed_job.result())
    print(executed_job.result().get_data())


IBMQ.enable_account(Qconfig.APItoken, url=Qconfig.config['url'])



