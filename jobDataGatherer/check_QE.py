from IBMQuantumExperience import IBMQuantumExperience
from Qconfig import *
from enum import IntEnum


class FilteredJobPart(IntEnum):
    backend_name = 0
    execution_date = 1
    results = 2


def get_done_jobs(limit):
    api = IBMQuantumExperience(APItoken)
    all_jobs = api.get_jobs(limit)
    done_jobs = [j for j in all_jobs if j['status'] == 'COMPLETED']

    return done_jobs


# filter_jobs_data returns a list of tuples with important info, such as backend name, execution data, and results
def filter_jobs_data(jobs):
    data = []
    for job in jobs:
        for qasm in job['qasms']:
            row = job['backend']['name'], qasm['result']['date'], qasm['result']['data']['counts']
            data.append(row)
    return data


def parse_filtered_job_to_string(datum):
    resultant_string = ""
    resultant_string += datum[FilteredJobPart.backend_name] + ","
    resultant_string += datum[FilteredJobPart.execution_date] + ","

    results_dict = datum[FilteredJobPart.results]

    for key in results_dict.keys():
        resultant_string += key + ":" + str(results_dict[key]) + ","

    resultant_string = resultant_string[:-1] + '\n'

    return resultant_string
