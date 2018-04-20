import check_QE

# Get finished jobs

jobs_num = 1240

my_jobs = check_QE.get_done_jobs(jobs_num)
my_data = check_QE.filter_jobs_data(my_jobs)

# Parse them to string

string_data = ""

for datum in my_data:
    string_data += check_QE.parse_filtered_job_to_string(datum)

# Save them to file

file = open("data.txt", "w")
file.write(string_data)
file.close()
