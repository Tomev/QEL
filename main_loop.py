# This file contains main loop for multiple quantum programs execution with changing backends.

from qiskit import QISKitError
import methods
from methods import consts
import time

########################
# Prepare circuits here.
########################

print('Circuit prepared for execution.')

##############################
# Assign circuits to run here.
##############################
circuits = ''

current_backend_index = 0

for iteration_number in range(0, consts.ITERATIONS_NUMBER):

    print('Iteration number: ', iteration_number)

    current_credits_number = methods.get_current_credits()

    # In case there are to little credits
    while current_credits_number < 3:
        print("Current credits number is", current_credits_number,
              'which is less than 3. Waiting 10 minutes to continue.')
        time.sleep(600)
        current_credits_number = methods.get_current_credits()

    print('Getting available backends...')
    available_backends = methods.get_available_remote_backends_names()

    # Actual execution call
    # IMPORTANT https://github.com/QISKit/qiskit-sdk-py/issues/247
    if __name__ == '__main__':
        try:
            backend = methods.get_backend_name_from_number(current_backend_index)

            while not available_backends.__contains__(backend):
                print(backend, ': Currently not available.')
                current_backend_index = (current_backend_index + 1) % len(consts.CONSIDERED_REMOTE_BACKENDS)
                backend = methods.get_backend_name_from_number(current_backend_index)
                print('Refreshing available backends list...')
                available_backends = methods.get_available_remote_backends_names()
                print('Trying another backend: ', backend)

            print("Executing quantum program on backend:", backend)
            methods.execute(circuits, backend)

            print("Program send for execution to ", backend, '.')
            current_backend_index = (current_backend_index + 1) % len(consts.CONSIDERED_REMOTE_BACKENDS)

        except QISKitError as ex:
            print('There was an error in the circuit!. Error = {}'.format(ex))

