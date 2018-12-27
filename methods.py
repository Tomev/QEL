from qiskit import execute, IBMQ, Aer
from IBMQuantumExperience import IBMQuantumExperience
import qiskit
import time
import pandas as pd

import Qconfig
import consts


def get_operational_remote_backends():
    operational_backends = IBMQ.backends(operational=True, filters=lambda x: not x.configuration().simulator)
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


def test_locally(circuits):
    backend = get_sim_backend_from_name("qasm_simulator")
    executed_job = execute_circuits(circuits, backend)

    for circuit in circuits:
        print(circuit.name)
        print(executed_job.result().get_counts(circuit))


def get_jobs_from_backend(backend_name, jobs_number=consts.JOBS_DOWNLOAD_LIMIT):
    backend = IBMQ.get_backend(backend_name)

    number_of_jobs_to_download = jobs_number
    downloaded_jobs = []
    number_of_jobs_to_skip = 0

    # Due to long connection times and a fail probability small download step is used

    while number_of_jobs_to_download > 0:

        print("Number of jobs to download left: %i." % number_of_jobs_to_download)

        number_of_jobs_to_download_now = min(consts.MAX_JOBS_SINGLE_DOWNLOAD_NUM, number_of_jobs_to_download)

        number_of_jobs_to_download -= number_of_jobs_to_download_now
        downloaded_jobs.extend(backend.jobs(limit=number_of_jobs_to_download_now, skip=number_of_jobs_to_skip, status='DONE'))
        number_of_jobs_to_skip += number_of_jobs_to_download_now

    return downloaded_jobs


def parse_job_to_report_string(job):
    job_string = ''

    job_id = job.job_id()
    circuit_names = [j.header.name for j in job.result().results]
    job_backend_name = job.backend().name()
    job_creation_date = job.creation_date()

    for circuit_name in circuit_names:
        job_string += job_id + consts.CSV_SEPARATOR
        job_string += job_backend_name + consts.CSV_SEPARATOR
        job_string += str(circuit_name) + consts.CSV_SEPARATOR
        job_string += job_creation_date + consts.CSV_SEPARATOR
        job_string += str(job.result().get_counts(circuit_name)) + '\n'

    return job_string


def report_to_csv(csv_file, report_file=consts.JOBS_FILE_NAME, sep = consts.CSV_SEPARATOR, lowercase_header = True):
    df = pd.read_csv(report_file, sep = sep)
    
    results=df.Results
    results = [eval(r) for r in results]
    results = pd.DataFrame.from_dict({i:results[i] for i in range(len(results))}, 'index')
    
    df_long = pd.melt(
        pd.concat([df, results], axis=1).drop('Results',1),
        list(set(df.columns)-{'Results'})
    )
    
    if(lowercase_header):
        df_long.columns = [c.lower() for c in df_long.columns]
    
    df_long.to_csv(csv_file, index=False)    
    
    
    
def get_chsh_circuits():
    q = qiskit.QuantumRegister(2)
    c = qiskit.ClassicalRegister(2)
    
    #circuit to prepare an entangled state
    bell = qiskit.QuantumCircuit(q, c)
    bell.h(q[0])
    bell.cx(q[0], q[1])
    bell.ry(np.pi/4, q[0])

    #circuits to measure q to c in different basis
    measure_zz = qiskit.QuantumCircuit(q, c)
    measure_zz.measure(q[0], c[0])
    measure_zz.measure(q[1], c[1])

    measure_xx = qiskit.QuantumCircuit(q, c)
    measure_xx.h(q[0])
    measure_xx.h(q[1])
    measure_xx.measure(q[0], c[0])
    measure_xx.measure(q[1], c[1])

    measure_zx = qiskit.QuantumCircuit(q, c)
    measure_zx.h(q[0])
    measure_zx.measure(q[0], c[0])
    measure_zx.measure(q[1], c[1])

    measure_xz = qiskit.QuantumCircuit(q, c)
    measure_xz.h(q[1])
    measure_xz.measure(q[0], c[0])
    measure_xz.measure(q[1], c[1])

    measure = [measure_zz, measure_zx, measure_xx, measure_xz]


    chsh_circuits = []
    for m in measure:
        chsh_circuits.append(bell + m)

    #set circuits names
    chsh_circuits[0].name = 'CHSH_test_ZZ'
    chsh_circuits[1].name = 'CHSH_test_ZX'
    chsh_circuits[2].name = 'CHSH_test_XX'
    chsh_circuits[3].name = 'CHSH_test_XZ'
    
    return(chsh_circuits)

def run_main_loop_with_chsh_test(circuits):
    run_main_loop(circuits+get_chsh_circuits())
  
IBMQ.enable_account(Qconfig.APItoken, url=Qconfig.config['url'])



