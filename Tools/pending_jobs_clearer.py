import consts
from qiskit import IBMQ

backend = IBMQ.load_account().backends(consts.CONSIDERED_REMOTE_BACKENDS[0])[0]

print(f'Clearing backend {backend}.')

downloaded_jobs = []
max_download_number = 10
download_number = min(max_download_number, consts.MAX_JOBS_SINGLE_DOWNLOAD_NUM)

# This
downloaded_jobs.extend(backend.jobs(limit=5, status='QUEUED'))
downloaded_jobs.extend(backend.jobs(limit=5, status='RUNNING'))

print(f'Got {len(downloaded_jobs)} jobs.\n')

for j in downloaded_jobs:
    j.cancel()
    print('CANCELLED')

print('\nClearing finished.')
