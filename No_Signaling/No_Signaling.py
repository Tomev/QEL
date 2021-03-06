import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from CHSH.CHSH_XY import get_symmetric_chsh_circuits, get_symmetric_chsh_test_circuits
from Mermin.Mermin import get_mermin_circuits, get_mermin_test_circuits
from SanityCheck.SanityCheck import get_sc_n2_circuits, get_sc_n3_circuits, get_n2_calibration_circuits, \
    get_n3_calibration_circuits
from methods import test_locally

chsh_circuits = get_sc_n2_circuits() + get_symmetric_chsh_circuits(
    8) + get_symmetric_chsh_test_circuits() + get_n2_calibration_circuits()
mermin_circuits = get_sc_n3_circuits() + get_mermin_circuits(
    8) + get_mermin_test_circuits() + get_n3_calibration_circuits()

# no_signaling_circuits = [chsh_circuits, mermin_circuits]
no_signaling_circuits = mermin_circuits

# print(f'CHSH Experiment Circuits Length: {len(chsh_circuits)}')
print(f'Mermin Experiment Circuits Length: {len(mermin_circuits)}')

print(f'No_signaling_experiments num: {len(no_signaling_circuits)}')

# run_main_loop(no_signaling_circuits)
# run_main_loop_with_chsh_test(circuits)
test_locally(no_signaling_circuits, True, False, 1)
