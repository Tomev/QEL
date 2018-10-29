import check_QE
from qiskit import *
import methods

# Get finished jobs...

jobs_num = 1

# print(methods.get_operational_remote_backends())

backend5 = IBMQ.get_backend('ibmqx4')
downloaded_jobs = backend5.jobs(jobs_num)

for job in downloaded_jobs:
    print(format(job.job_id()))
    print(job.creation_date())
    print(job.result().get_names())
    print(job.backend().name())
    #print(job.result().get_data())



my_jobs = check_QE.get_done_jobs(jobs_num)
my_data = check_QE.filter_jobs_data(my_jobs)

string_data = ""

filtered_job_keys = my_data[0].keys()

# Create a header line...

for key in filtered_job_keys:
    string_data = string_data + key + check_QE.CSV_SEPARATOR

# Make last char a new line instead of separator...
string_data = string_data[:-1] + '\n'

# Parse them to string...

for datum in my_data:
    string_data += check_QE.parse_filtered_job_to_string(datum, filtered_job_keys)

# Save them to file...

file = open("data.csv", "w")
file.write(string_data)
file.close()
