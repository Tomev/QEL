from qiskit.tools.monitor import backend_monitor

from ..methods import get_backend_from_name

backend = get_backend_from_name('ibmq_vigo')
backend_monitor(backend)
