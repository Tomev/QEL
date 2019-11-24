from qiskit import execute, IBMQ, Aer, QuantumCircuit, QuantumRegister, ClassicalRegister, exceptions
from qiskit.providers.aer import noise
from qiskit.providers.ibmq.job.ibmqjob import IBMQJob, JobStatus
from IBMQuantumExperience import IBMQuantumExperience
import numpy as np
import time
import pandas as pd
import os
import datetime

import Qconfig
import consts

from qiskit.ignis.mitigation.measurement import (complete_meas_cal,
                                                 CompleteMeasFitter,
                                                 MeasurementFilter)


def get_operational_remote_backends():
    operational_backends = acc.backends(operational=True, filters=lambda x: not x.configuration().simulator)
    return operational_backends


def get_backends_names(backends):
    names = []

    for backend in backends:
        names.append(backend.name())

    return names


def get_backend_from_name(name):
    return acc.backends(name)[0]


def get_sim_backend_from_name(name):
    return Aer.get_backend(name)


# Legacy
def get_current_credits():
    # return 3  # placeholder, until I get answer from IBM
    # This method will cause errors, as IBMQuantumExperience server is now shut down.
    api = IBMQuantumExperience(token=Qconfig.APItoken, config=Qconfig.config)
    return api.get_my_credits()['remaining']


# Legacy
def get_backend_name_from_number(backend_index):
    backend_index = backend_index % len(consts.CONSIDERED_REMOTE_BACKENDS)
    return consts.CONSIDERED_REMOTE_BACKENDS[backend_index]


def execute_circuits(circuits, backend, use_mapping=False, noise_model=None):
    if use_mapping:
        real_chip = get_backend_from_name(consts.CONSIDERED_REMOTE_BACKENDS[0])
        mapping = real_chip.configuration().coupling_map
        print("Used mapping:")
        print(mapping)
        return execute(circuits, backend, shots=consts.SHOTS, coupling_map=mapping)
    elif noise_model is not None:
        real_chip = get_backend_from_name(consts.CONSIDERED_REMOTE_BACKENDS[0])
        mapping = real_chip.configuration().coupling_map
        basis_gates = noise_model.basis_gates
        return execute(circuits, backend, noise_model=noise_model, shots=consts.SHOTS,
                       basis_gates=basis_gates, coupling_map=mapping)
    else:
        return execute(circuits, backend, shots=consts.SHOTS)


def run_main_loop(circuits):
    current_backend_index = 0
    wait_time_in_minutes = 5

    if not os.path.isfile(os.path.join(os.path.dirname(__file__), 'current_iteration_holder.txt')):
        file = open(os.path.join(os.path.dirname(__file__), 'current_iteration_holder.txt'), "a")
        file.write('0')
        file.close()

    file = open(os.path.join(os.path.dirname(__file__), 'current_iteration_holder.txt'), "r")
    line = file.readline()
    iterations_done = int(line)
    file.close()

    while iterations_done < consts.ITERATIONS_NUMBER:

        print(f'Iteration number: { iterations_done}')

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

            job = execute_circuits(circuits, get_backend_from_name(backend_name))

            while job.status() == JobStatus.INITIALIZING:
                print(job.status())
                time.sleep(10)

            print("Program sent for execution to ", backend_name, '.')
            current_backend_index = (current_backend_index + 1) % len(consts.CONSIDERED_REMOTE_BACKENDS)

        except BaseException as ex:
            print('There was an error in the circuit!. Error = {}'.format(ex))
            print(f'Waiting {wait_time_in_minutes} minute(s) before next try.')
            time.sleep(wait_time_in_minutes * 60)
            continue

        iterations_done += 1
        line = str(iterations_done)
        print(f'Writing to file: {line}')
        file = open(os.path.join(os.path.dirname(__file__), 'current_iteration_holder.txt'), 'w')
        file.write(line)
        file.close()

    reset_jobs_counter()


def reset_jobs_counter():
    if os.path.isfile(os.path.join(os.path.dirname(__file__), 'current_iteration_holder.txt')):
        os.remove(os.path.join(os.path.dirname(__file__), 'current_iteration_holder.txt'))


def test_locally(circuits, use_mapping=False, save_to_file=False, number_of_simulations=1):
    backend = get_sim_backend_from_name("qasm_simulator")

    if save_to_file:
        simulation_report_content = consts.JOBS_REPORT_HEADER

        for i in range(number_of_simulations):
            executed_job = execute_circuits(circuits, backend, use_mapping)
            simulation_report_content += parse_job_to_report_string(executed_job)
            print(f'Simulation {i + 1} done.')

        # Save gathered data to file.
        file = open("sim_report.csv", "w")
        file.write(simulation_report_content)
        file.close()
        print("Report saved!")
    else:
        for circuit in circuits:
            executed_job = execute_circuits(circuits, backend, use_mapping)
            print(circuit.name)
            print(executed_job.result().get_counts(circuit))


def test_locally_with_noise(circuits, save_to_file=False, number_of_simulations=1):
    properties = get_backend_from_name(consts.CONSIDERED_REMOTE_BACKENDS[0]).properties()
    noise_model = noise.device.basic_device_noise_model(properties)

    backend = get_sim_backend_from_name("qasm_simulator")

    if save_to_file:
        simulation_report_content = consts.JOBS_REPORT_HEADER

        for i in range(number_of_simulations):
            executed_job = execute_circuits(circuits, backend, noise_model=noise_model)
            simulation_report_content += parse_job_to_report_string(executed_job)
            print(f'Simulation {i + 1} done.')

        # Save gathered data to file.
        file = open("sim_report.csv", "w")
        file.write(simulation_report_content)
        file.close()
        print("Report saved!")
    else:
        for circuit in circuits:
            executed_job = execute_circuits(circuits, backend, noise_model=noise_model)
            print(circuit.name)
            print(executed_job.result().get_counts(circuit))


def test_locally_with_error_mitigation(circuits, save_to_file=False, number_of_simulations=1):
    properties = get_backend_from_name(consts.CONSIDERED_REMOTE_BACKENDS[0]).properties()
    noise_model = noise.device.basic_device_noise_model(properties)

    backend = get_sim_backend_from_name("qasm_simulator")

    if save_to_file:
        simulation_report_content = consts.JOBS_REPORT_HEADER
        mitigation_report_content = consts.JOBS_REPORT_HEADER

        for i in range(number_of_simulations):
            executed_job = execute_circuits(circuits, backend, noise_model=noise_model)
            error_mitigation_filters = get_error_mitigation_filters(executed_job)

            simulation_report_content += parse_job_to_report_string(executed_job)
            mitigation_report_content += get_mitigation_report_string(executed_job)

            print(f'Simulation {i + 1} done.')

            for circuit in circuits:
                executed_job = execute_circuits(circuits, backend, noise_model=noise_model)
                print(circuit.name)
                raw_counts = executed_job.result().get_counts(circuit)

                index = len(list(raw_counts.keys())[0])
                meas_filter = error_mitigation_filters[index]
                mitigated_counts = meas_filter.apply(raw_counts)

                print("Results without mitigation:", raw_counts)
                print("Results with mitigation:", {l: int(mitigated_counts[l]) for l in mitigated_counts})

        # Save gathered data to file.
        file = open("sim_report.csv", "w")
        file.write(simulation_report_content)
        file.close()

        file = open('raw_mitigation_jobs_report.csv', 'w')
        file.write(mitigation_report_content)
        file.close()

        print("Report saved!")
    else:
        for circuit in circuits:
            executed_job = execute_circuits(circuits, backend, noise_model=noise_model)
            error_mitigation_filters = get_error_mitigation_filters(executed_job)
            print(circuit.name)
            raw_counts = executed_job.result().get_counts(circuit)

            index = len(list(raw_counts.keys())[0])
            meas_filter = error_mitigation_filters[index]
            mitigated_counts = meas_filter.apply(raw_counts)

            print("Results without mitigation:", raw_counts)
            print("Results with mitigation:", {l: int(mitigated_counts[l]) for l in mitigated_counts})


def get_jobs_from_backend(backend_name, jobs_number=consts.JOBS_DOWNLOAD_LIMIT):
    backend = IBMQ.load_account().backends(backend_name)[0]

    number_of_jobs_to_download = jobs_number
    downloaded_jobs = []
    number_of_jobs_to_skip = 0
    max_download_number = 10
    download_number = min(max_download_number, consts.MAX_JOBS_SINGLE_DOWNLOAD_NUM)

    while number_of_jobs_to_download > 0:
        print("Number of jobs to download left: %i." % number_of_jobs_to_download)

        number_of_jobs_to_download_now = min(download_number, number_of_jobs_to_download)

        number_of_jobs_to_download -= number_of_jobs_to_download_now
        downloaded_jobs.extend(
            backend.jobs(limit=number_of_jobs_to_download_now, skip=number_of_jobs_to_skip, status='DONE'))
        number_of_jobs_to_skip += number_of_jobs_to_download_now

    return downloaded_jobs


def parse_job_to_report_string(job):
    job_string = ''

    job_id = job.job_id()
    circuit_names = [j.header.name for j in job.result().results]
    job_backend_name = job.backend().name()

    if type(job).__name__ == 'AerJob':
        job_creation_date = '-'
    else:
        job_creation_date = job.creation_date()

    for circuit_name in circuit_names:
        job_string += job_id + consts.CSV_SEPARATOR
        job_string += job_backend_name + consts.CSV_SEPARATOR
        job_string += str(circuit_name) + consts.CSV_SEPARATOR
        job_string += job_creation_date + consts.CSV_SEPARATOR
        job_string += str(job.result().get_counts(circuit_name)) + '\n'

    return job_string


def get_mitigation_report_string(job):
    job_string = ''

    job_id = job.job_id()
    circuit_names = [j.header.name for j in job.result().results]
    job_backend_name = job.backend().name()

    if type(job).__name__ == 'AerJob':
        job_creation_date = '-'
    else:
        job_creation_date = job.creation_date()

    error_mitigation_filters = get_error_mitigation_filters(job)

    for circuit_name in circuit_names:
        job_string += job_id + consts.CSV_SEPARATOR
        job_string += job_backend_name + consts.CSV_SEPARATOR
        job_string += str(circuit_name) + consts.CSV_SEPARATOR
        job_string += job_creation_date + consts.CSV_SEPARATOR

        raw_counts = job.result().get_counts(circuit_name)
        index = len(list(raw_counts.keys())[0])
        meas_filter = error_mitigation_filters[index]
        mitigated_counts = meas_filter.apply(raw_counts)

        job_string += str(mitigated_counts) + '\n'

    return job_string


def report_to_csv(csv_file, report_file=consts.JOBS_FILE_NAME, sep=consts.CSV_SEPARATOR, lowercase_header=True):
    data_file = pd.read_csv(report_file, sep=sep)

    # Evaling string representations of dictionaries in 'Results' column ("{"00":500, "11":524}")
    results = data_file.Results
    results = [eval(r) for r in results]

    # Creating a data frame with results in the long format (1, "00", 500 // 1, "11", 524)
    # Auxiliary column "row_num" contains row index from the original data frame - to enable joining
    # Column "variable" contains keys from the dictionaries (names of states)
    # Column "value" contains their respective values (count)
    results = pd.DataFrame([[i, str(r), results[i][r]] for i in range(len(results)) for r in results[i]],
                           columns=['row_num', 'variable', 'value'])

    # Joining results with other experimental data
    df_long = data_file.merge(results, left_index=True, right_on='row_num').drop(['row_num', 'Results'], 1)

    # Converting uppercase in header names to lowercase
    if lowercase_header:
        df_long.columns = [c.lower() for c in df_long.columns]

    df_long.to_csv(csv_file, index=False)


def add_measure_in_base(qc: QuantumCircuit, base: str):

    base = ''.join(reversed(base.upper()))

    for i in range(len(base)):
        if base[i] == 'X':
            qc.h(qc.qubits[i])
        elif base[i] == 'Y':
            qc.s(qc.qubits[i]).inverse()
            qc.h(qc.qubits[i])

    qc.measure(qc.qubits, qc.clbits)

    base = ''.join(reversed(base.upper()))

    input_circ_name_parts = qc.name.split('_')

    if input_circ_name_parts[-1] == 'B':
        new_name = ''
        for i in range(len(input_circ_name_parts) - 1):
            new_name = new_name + input_circ_name_parts[i] + '_'
        qc.name = new_name + base + '_B'
    else:
        qc.name = qc.name + "_" + base

    return qc


def get_chsh_circuits():
    q = QuantumRegister(2)
    c = ClassicalRegister(2)

    # Circuit to prepare an entangled state.
    bell = QuantumCircuit(q, c)
    bell.h(q[0])
    bell.cx(q[0], q[1])
    bell.ry(np.pi / 4, q[0])

    # Circuits to measure q to c in different basis.
    bases = ['ZZ', 'ZX', 'XX', 'XZ']

    chsh_circuits = []
    for b in bases:
        chsh_circuits.append(add_measure_in_base(bell.copy(), b))

    # Set circuits names.
    chsh_circuits[0].name = 'CHSH-test_ZZ'
    chsh_circuits[1].name = 'CHSH-test_ZX'
    chsh_circuits[2].name = 'CHSH-test_XX'
    chsh_circuits[3].name = 'CHSH-test_XZ'

    return chsh_circuits


def run_main_loop_with_chsh_test(circuits):
    run_main_loop(circuits + get_chsh_circuits())


def create_circuit_from_qasm(qasm_file_path):
    return QuantumCircuit.from_qasm_file(qasm_file_path)


# Legacy
def custom_backend_monitor(backend):
    # Custom version of qiskit 10.1 backend monitor.

    config = backend.configuration().to_dict()
    props = backend.properties().to_dict()

    offset = '    '
    sep = ' / '

    backend_info = ''

    qubit_header = 'Qubits [Name / Freq / T1 / T2 / U1 err / U2 err / U3 err / Readout err]'

    backend_info = backend_info + qubit_header + '\n'
    backend_info = backend_info + '-' * len(qubit_header) + '\n'

    for qub in range(len(props['qubits'])):
        name = 'Q%s' % qub
        qubit_data = props['qubits'][qub]
        gate_data = props['gates'][3 * qub:3 * qub + 3]
        t1_info = qubit_data[0]
        t2_info = qubit_data[1]
        freq_info = qubit_data[2]
        readout_info = qubit_data[3]

        freq = str(round(freq_info['value'], 5)) + ' ' + freq_info['unit']
        T1 = str(round(t1_info['value'], 5)) + ' ' + t1_info['unit']
        T2 = str(round(t2_info['value'], 5)) + ' ' + t2_info['unit']
        U1 = str(round(gate_data[0]['parameters'][0]['value'], 5))
        U2 = str(round(gate_data[1]['parameters'][0]['value'], 5))
        U3 = str(round(gate_data[2]['parameters'][0]['value'], 5))
        readout_error = str(round(readout_info['value'], 5))
        qstr = sep.join([name, freq, T1, T2, U1, U2, U3, readout_error])

        backend_info = backend_info + offset + qstr + '\n'

    backend_info = backend_info + '\n'
    multi_qubit_gates = props['gates'][3 * config['n_qubits']:]
    multi_header = 'Multi-Qubit Gates [Name / Type / Gate Error]'

    backend_info = backend_info + multi_header + '\n'
    backend_info = backend_info + '-' * len(multi_header) + '\n'

    for gate in multi_qubit_gates:
        name = gate['name']
        ttype = gate['gate']
        error = str(round(gate['parameters'][0]['value'], 5))
        mstr = sep.join([name, ttype, error])
        backend_info = backend_info + offset + mstr + '\n'

    return backend_info


# Legacy
def save_calibration_data(backend_name, data):
    now = datetime.datetime.now()
    file_name = backend_name + "_" + now.strftime("%Y-%m-%d_%H-%M") + ".txt"

    file_path = os.path.join(os.path.dirname(__file__), 'CalibrationHistory\\' + file_name)

    f = open(file_path, "w+")
    f.write(data)
    f.close()


def get_error_mitigation_filters(job):

    if type(job).__name__ == 'AerJob':
        job_creation_date = '-'
        backend_name = consts.CONSIDERED_REMOTE_BACKENDS[0]
    else:
        job_creation_date = job.creation_date()
        backend_name = job.backend().name()

    properties = get_backend_from_name(backend_name).properties(job_creation_date)
    noise_model = noise.device.basic_device_noise_model(properties)
    filters = dict()

    qubits_lists = []
    # This could possibly be a one liner, but I find the loops easier to understand
    for i in range(len(properties.qubits)):
        q_list = []
        for j in range(i + 1):
            q_list.append(j)
        qubits_lists.append(q_list)

    i = 1  # Start from 1, as it would be dictionary accessed by result state length

    for q_list in qubits_lists:
        filters[i] = generate_error_mitigation_filter(q_list, noise_model)
        i += 1

    return filters


def generate_error_mitigation_filter(q_list, noise_model):
    backend = get_sim_backend_from_name("qasm_simulator")
    qr = QuantumRegister(5)
    meas_cals, state_labels = complete_meas_cal(qubit_list=q_list, qr=qr)
    calibration_job = execute(meas_cals, backend=backend, shots=8192, noise_model=noise_model)
    cal_results = calibration_job.result()
    meas_fitter = CompleteMeasFitter(cal_results, state_labels)
    em_filter = meas_fitter.filter
    return em_filter


IBMQ.save_account(Qconfig.APItoken, overwrite=True)
acc = IBMQ.load_account()
acc.credentials
