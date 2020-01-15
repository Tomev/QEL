# This is parser only for data reports used by A for analysis

import sys
sys.path.append('..\\')
from methods import report_to_csv

file_result_name = 'jobs_report.csv'

# report_file = JOBS_FILE_NAME  # Default value

report_file = 'raw_jobs_report.csv'
report_to_csv(file_result_name, report_file=report_file)

file_result_name = 'm_jobs_report.csv'

report_file = 'raw_mitigation_jobs_report.csv'
report_to_csv(file_result_name, report_file=report_file)
