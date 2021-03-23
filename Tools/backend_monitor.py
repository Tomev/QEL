import os
import sys

from qiskit.tools.monitor import backend_monitor

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from methods import get_backend_from_name

backend = get_backend_from_name('ibmq_vigo')
backend_monitor(backend)
