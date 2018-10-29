import methods, consts

# Select desired backends.
considered_backends_names = consts.CONSIDERED_REMOTE_BACKENDS

report_content = consts.JOBS_REPORT_HEADER

# Get jobs data.
for backend_name in considered_backends_names:
    backends_jobs = methods.get_jobs_from_backend(backend_name)

    for job in backends_jobs:
        report_content += methods.parse_job_to_report_string(job)

# Save gathered data to file.
file = open("jobs_report.csv", "w")
file.write(report_content)
file.close()
