from Qconfig import reports_postfix

SHOTS = 8192  # Standard was 1024
ITERATIONS_NUMBER = 1

# Job gatherer
CSV_SEPARATOR = ';'
JOBS_DOWNLOAD_LIMIT = 500
MAX_JOBS_SINGLE_DOWNLOAD_NUM = 10  # 10 is max.
JOBS_REPORT_HEADER = 'ID;Backend;Circuit;Date;Results\n'
JOBS_FILE_NAME = f"raw_jobs_report_{reports_postfix}.csv"
M_JOBS_FILE_NAME = f"raw_mitigation_jobs_report_{reports_postfix}.csv"
