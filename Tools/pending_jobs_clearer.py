import sys

sys.path.append('..')

import consts
from qiskit import IBMQ

backend = IBMQ.load_account().backends(consts.CONSIDERED_REMOTE_BACKENDS[0])[0]

print(f'Clearing backend {backend}.')

jobs_to_cancel = []

# This may need to include more statuses.
jobs_to_cancel.extend(backend.jobs(limit=5, status='QUEUED'))
jobs_to_cancel.extend(backend.jobs(limit=5, status='RUNNING'))

print(f'Got {len(jobs_to_cancel)} jobs.\n')

for j in jobs_to_cancel:
    j.cancel()
    print('CANCELLED')

print('\nClearing finished.')
