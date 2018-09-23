import check_QE

# Get finished jobs...

jobs_num = 15

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
