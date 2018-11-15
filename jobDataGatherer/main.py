import methods
import consts
import time

# Select desired backends.
considered_backends_names = consts.CONSIDERED_REMOTE_BACKENDS
report_content = consts.JOBS_REPORT_HEADER

# Get jobs data.
for backend_name in considered_backends_names:
    print(f'Started job gathering from {backend_name}.')
    job_gathering_time = time.time()
    backends_jobs = methods.get_jobs_from_backend(backend_name)
    job_gathering_time = time.time() - job_gathering_time
    print(f"Jobs gathered from {backend_name} finished in {job_gathering_time} s.")

    i = 0
    jobs_parsing_time = time.time()
    for job in backends_jobs:
        job_parsing_time = time.time()
        report_content += methods.parse_job_to_report_string(job)
        job_parsing_time = time.time() - job_parsing_time
        print(f"Job {i} parsing finished in {job_parsing_time} s.")
        i += 1
    jobs_parsing_time = time.time() - jobs_parsing_time
    print(f"All jobs parsing finished in {jobs_parsing_time} s.")
    print(f"Average job parsing time is {jobs_parsing_time / len(backends_jobs)} s.")


print("Starting report generation.")
report_generation_time = time.time()
# Save gathered data to file.
file = open("jobs_report.csv", "w")
file.write(report_content)
file.close()

report_generation_time = time.time() - report_generation_time
print(f'Report generated in {report_generation_time} s.')
