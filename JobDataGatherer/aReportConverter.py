# This is parser only for data reports used by A for analysis

import sys
sys.path.append('..\\')
from methods import report_to_csv
from consts import JOBS_FILE_NAME

file_result_name = 'jobs_report.csv'

# report_file = JOBS_FILE_NAME  # Default value

report_file = JOBS_FILE_NAME
report_to_csv(file_result_name, report_file=report_file)
