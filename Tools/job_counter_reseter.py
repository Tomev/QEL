import os
import sys

from methods import reset_jobs_counter

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

reset_jobs_counter()
