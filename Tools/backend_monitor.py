from qiskit import IBMQ
from qiskit.tools.monitor import backend_monitor

IBMQ.load_accounts()

backend = IBMQ.get_backend('ibmqx2')
backend_monitor(backend)

backend = IBMQ.get_backend('ibmqx4')
backend_monitor(backend)
