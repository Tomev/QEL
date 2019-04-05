# Downloads last job in given backend and reports it's status
# One need to pass backend name as an argument

import sys
sys.path.append('..\\')
from methods import get_backend_from_name

if len(sys.argv) == 1:
    print("No backend specified.")
    exit()

backend = get_backend_from_name(sys.argv[1])
downloaded_job = backend.jobs(limit=1)
print(downloaded_job[0].status())
