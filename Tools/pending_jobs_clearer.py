import os
import sys

from qiskit import IBMQ
from qiskit.providers.jobstatus import JobStatus

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import consts

backend = IBMQ.load_account().backends(consts.CONSIDERED_REMOTE_BACKENDS[0])[0]

print(f'Clearing backend {backend}.')

jobs_to_cancel = []

# This may need to include more statuses.
jobs_to_cancel.extend(backend.jobs(limit=5, status=JobStatus.QUEUED))
jobs_to_cancel.extend(backend.jobs(limit=5, status=JobStatus.RUNNING))

if len(jobs_to_cancel) == 0:
    print('No jobs were found. Canceling last 5 jobs.')
    jobs_to_cancel.extend(backend.jobs(limit=5))

print(f'Got {len(jobs_to_cancel)} jobs to cancel.\n')

for j in jobs_to_cancel:
    print(j.status())
    if j.status() != JobStatus.CANCELLED:
        j.cancel()
        print('CANCELLED')
    else:
        print('Job was already cancelled.')

print('\nClearing finished.')
