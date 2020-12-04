# This gatherer will download and write jobs one at the time. Let it download jobs until certain date is met.

import sys
sys.path.append('..\\')
from os.path import isfile
from datetime import datetime
from methods import parse_job_to_report_string, report_to_csv, get_backend_from_name
from time import time
import consts


class SingleJobGatherer:
    backend_name = ""
    jobs_to_skip = 0

    def __init__(self, backend_name, jobs_to_skip):
        self.backend_name = backend_name
        self.jobs_to_skip = jobs_to_skip

    def get_single_job(self):
        backend = get_backend_from_name(self.backend_name)

        number_of_jobs_to_download = 1
        downloaded_job = backend.jobs(limit=number_of_jobs_to_download, skip=self.jobs_to_skip, status='DONE')

        return downloaded_job[0]

    @staticmethod
    def parse_date(date):
        # Parses date to list [year, month, day]
        date_parts = [int(date_part) for date_part in date.split("T")[0].split("-")]
        return datetime(date_parts[0], date_parts[1], date_parts[2])


jobs_gathering_time = time()
initialization_time = time()
# First, if no report is present, create one
current_line = consts.JOBS_REPORT_HEADER

if not isfile(consts.JOBS_FILE_NAME):
    file = open(consts.JOBS_FILE_NAME, "w+")
    file.write(current_line)
    file.close()

# Now that file is surely there what we want to do is count number of distinct ids, to know how many jobs are already
# gathered and how many should be omitted
file = open(consts.JOBS_FILE_NAME, "r")
distinct_ids = set()
current_line = file.readline()  # Omitting header
current_line = file.readline()

while current_line:
    distinct_ids.add(current_line.split(';')[0])
    current_line = file.readline()

file.close()

# Now we're ready to initialize job gatherer
# TR TODO: Note that in case of multiple backends this file should be updated

job_gatherer = SingleJobGatherer(consts.CONSIDERED_REMOTE_BACKENDS[0], len(distinct_ids))
year = 2019
month = 5
day = 8
end_date = datetime(year, month, day)

initialization_time = time() - initialization_time
print(f"Gatherer initialized in {initialization_time} second(s).")

#print("Printing job")
#file = open("job_result.txt", "a")
#file.write(str(job_gatherer.get_single_job().result()))
#file.close()
#print("Done")

while True:
    job_gathering_time = time()

    current_line = parse_job_to_report_string(job_gatherer.get_single_job())
    job_gatherer.jobs_to_skip += 1

    # If current job date is before end_date, finish
    current_date = job_gatherer.parse_date(current_line.split(';')[3])
    print(f"Current date: {current_date}.")

    # When to quit
    if current_date < end_date:
        break

    # Else write it to the file
    file = open(consts.JOBS_FILE_NAME, "a")
    file.write(current_line)
    file.close()

    job_gathering_time = time() - job_gathering_time
    print(f"Job data gathered and written in {job_gathering_time} second(s).")

    # And check if desired number of jobs is satisfied and break is so.
    if job_gatherer.jobs_to_skip >= consts.JOBS_DOWNLOAD_LIMIT:
        break

    print(f"Skipping {job_gatherer.jobs_to_skip} jobs.")

jobs_gathering_time = time() - jobs_gathering_time
print(f"Jobs gathering and writing finished in {jobs_gathering_time} second(s).")

file_result_name = '.csv'
report_to_csv(file_result_name)
