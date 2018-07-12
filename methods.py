from qiskit import available_backends, get_backend, execute, register
from IBMQuantumExperience import IBMQuantumExperience
import qiskit
import time

import Qconfig
import consts


def get_remote_backends_names():
    return available_backends({'local': False, 'simulator': False})


def get_available_remote_backends_names():
    remote_backends_names = get_remote_backends_names()
    available_remote_backends_names = []

    for index in range(len(remote_backends_names) - 1, 0 - 1, -1):
        backend = get_backend_from_name(remote_backends_names[index])
        if backend.status['operational']:
            available_remote_backends_names.append(backend.status['name'])

    return available_remote_backends_names


def get_backend_from_name(name):
    return get_backend(name)


def get_current_credits():
    api = IBMQuantumExperience(token=Qconfig.APItoken, config=Qconfig.config)
    return api.get_my_credits()['remaining']


def get_backend_name_from_number(backend_index):
    backend_index = backend_index % len(consts.CONSIDERED_REMOTE_BACKENDS)
    return consts.CONSIDERED_REMOTE_BACKENDS[backend_index]


def execute_circuits(circuits, backend_name):
    return execute(circuits, backend=backend_name, shots=consts.SHOTS)


def test_get_remote_backends_names():
    # Only naively checks if size of returned list is greater than 0. Most of the time will work well, but can be
    # false negative.
    assert (len(get_remote_backends_names()) > 0)


def test_get_backend_from_name():
    # Check if class of returned object is identical to expected.
    assert(isinstance(get_backend('ibmqx4'), qiskit.backends.ibmq.ibmqbackend.IBMQBackend))


def test_get_available_remote_backends():
    # Naive check. Most of the time will work well, but can be false negative.
    assert (len(get_available_remote_backends_names()) <= len(get_remote_backends_names()))


def test_get_current_credits():
    assert(get_current_credits() >= 0)


def run_main_loop(circuits):
    current_backend_index = 0

    for iteration_number in range(0, consts.ITERATIONS_NUMBER):

        print('Iteration number: ', iteration_number)

        current_credits_number = get_current_credits()

        # In case there are to little credits
        while current_credits_number < 3:
            print("Current credits number is", current_credits_number,
                  'which is less than 3. Waiting 1 hour to continue.')
            time.sleep(6 * 600)
            current_credits_number = get_current_credits()

        print('Getting available backends...')
        available_remote_backends = get_available_remote_backends_names()

        # Actual execution call
        # IMPORTANT https://github.com/QISKit/qiskit-sdk-py/issues/247
        # if __name__ == '__main__':
        try:
            backend = get_backend_name_from_number(current_backend_index)

            while not available_remote_backends.__contains__(backend):
                print(backend, ': Currently not available.')
                current_backend_index = (current_backend_index + 1) % len(consts.CONSIDERED_REMOTE_BACKENDS)
                backend = get_backend_name_from_number(current_backend_index)
                print('Refreshing available backends list...')
                available_remote_backends = get_available_remote_backends_names()
                print('Trying another backend: ', backend)

            print("Executing quantum program on backend:", backend)
            execute_circuits(circuits, backend)

            print("Program send for execution to ", backend, '.')
            current_backend_index = (current_backend_index + 1) % len(consts.CONSIDERED_REMOTE_BACKENDS)

        except qiskit.QISKitError as ex:
            print('There was an error in the circuit!. Error = {}'.format(ex))


register(Qconfig.APItoken, Qconfig.config['url'])



