SHOTS = 8192  # Standard was 1024
MAX_CREDITS = 3
CONSIDERED_REMOTE_BACKENDS = ['ibmqx2']
#CONSIDERED_REMOTE_BACKENDS = ['ibmqx4']
ITERATIONS_NUMBER = 1000

# Job gatherer
CSV_SEPARATOR = ';'
JOBS_DOWNLOAD_LIMIT = 1000
MAX_JOBS_SINGLE_DOWNLOAD_NUM = 200  # Should be lowered is case of problems. 200 is max.
JOBS_REPORT_HEADER = 'ID;Backend;Circuit;Date;Results\n'
JOBS_FILE_NAME = "jobs_report.csv"
