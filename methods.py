from qiskit import available_backends, get_backend, execute, register
from IBMQuantumExperience import IBMQuantumExperience
import qiskit


import Qconfig
import consts


def get_remote_backends_names():
    return available_backends({'local': False, 'simulator': False})


def get_available_remote_backends_names():
    remote_backends_names = get_remote_backends_names()
    available_remote_backends_names = []

    for index in range(len(remote_backends_names) - 1, 0 - 1, -1):
        if get_backend_from_name(remote_backends_names[index]).status['available']:
            available_remote_backends_names.append(remote_backends_names[index])

    return available_remote_backends_names


def get_backend_from_name(name):
    return get_backend(name)


def get_current_credits():
    api = IBMQuantumExperience(token=Qconfig.APItoken, config=Qconfig.config)
    return api.get_my_credits()['remaining']


def get_backend_name_from_number(backend_index):
    backend_index = backend_index % len(consts.CONSIDERED_REMOTE_BACKENDS)
    return consts.CONSIDERED_REMOTE_BACKENDS[backend_index]


def execute_circuits(circuits, backend_name, shots_num):
    return execute(circuits, backend=backend_name, shots=shots_num)

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


register(Qconfig.APItoken, Qconfig.config['url'])



