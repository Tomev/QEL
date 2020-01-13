import os
from datetime import datetime

desired_date = datetime.strptime('2019-12-20T20:00:00', '%Y-%m-%dT%H:%M:%S')

report = 'ID;Backend;Circuit;Date;Results\n'
mitigation_report = 'ID;Backend;Circuit;Date;Results\n'


def get_report_string_from_file(file_path):
    opened_file = open(file_path)

    line = opened_file.readline()  # Omit first line of report
    line = opened_file.readline()

    report_str = ''

    while line:
        job_date = datetime.strptime(line.split(';')[3], '%Y-%m-%dT%H:%M:%S.%fZ')
        if job_date > desired_date:
            report_str += line
        line = opened_file.readline()

    opened_file.close()
    return report_str


for file in os.listdir(os.getcwd()):
    if file.startswith('raw_jobs'):
        report += get_report_string_from_file(file)
    elif file.startswith('raw_mitigation'):
        mitigation_report += get_report_string_from_file(file)
    else:
        print(f'Ignoring: {file}.')


file = open('raw_jobs_report.csv', 'w')
file.write(report)
file.close()

file = open('raw_mitigation_jobs_report.csv', 'w')
file.write(mitigation_report)
file.close()

print('Launching aReportConverter.')

os.system('python aReportConverter.py')

print('Finished.')
