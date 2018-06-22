from IBMQuantumExperience import IBMQuantumExperience
from Qconfig import *
from enum import IntEnum
from consts import CSV_SEPARATOR


class FilteredJobPart(IntEnum):
    backend_name = 0
    execution_date = 1
    results = 2


def get_done_jobs(limit):
    api = IBMQuantumExperience(APItoken)
    all_jobs = api.get_jobs(limit)
    done_jobs = [j for j in all_jobs if j['status'] == 'COMPLETED']

    return done_jobs


# filter_jobs_data returns a dictionary with selected important info, such as backend name, execution date and results...
def filter_jobs_data(jobs):
    data = []
    for job in jobs:
        for qasm in job['qasms']:
            row = dict()
            row['backend_name'] = job['backend']['name']
            row['date'] = qasm['result']['date']
            row['results'] = qasm['result']['data']['counts']
            data.append(row)
    return data


def parse_filtered_job_to_string(datum_dict, ordered_keys):

    resultant_string = ''

    for key in ordered_keys:
        resultant_string = resultant_string + str(datum_dict[key]) + CSV_SEPARATOR

    # Make last char a new line instead of separator...
    resultant_string = resultant_string[:-1] + '\n'

    return resultant_string
