# This is parser only for data reports used by A for analysis

import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from methods import report_to_csv

file_result_name = 'jobs_report.csv'

# report_file = JOBS_FILE_NAME  # Default value

report_file = 'raw_jobs_report.csv'

report_to_csv(file_result_name, report_file=report_file)

file_result_name = 'm_jobs_report.csv'

report_file = 'raw_mitigation_jobs_report.csv'
report_to_csv(file_result_name, report_file=report_file)
