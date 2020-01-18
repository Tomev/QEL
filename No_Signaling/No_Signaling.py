import sys
sys.path.append('..')
import CHSH.CHSH_XY as CHSH
from SanityCheck.SanityCheck import get_sc_circuits
from Mermin.mermin_test import get_mermin_circuits
from methods import run_main_loop, run_main_loop_with_chsh_test, test_locally, test_locally_with_noise, get_chsh_circuits

#chsh_circuits = CHSH.get_chsh_circuits(8) + get_chsh_circuits()
#complementary_circuits = get_mermin_circuits() + get_sc_circuits() + get_chsh_circuits()
#circuits = [chsh_circuits, complementary_circuits]

no_signaling_circuits = CHSH.get_chsh_circuits(8) + get_chsh_circuits() + get_sc_circuits()

print(f'SC: {len(get_sc_circuits())}')
print(f'CHSH: {len(CHSH.get_chsh_circuits(8))}')
print(f'CHSH_TEST: {len(get_chsh_circuits())}')

print(len(no_signaling_circuits))

run_main_loop([no_signaling_circuits])
#run_main_loop_with_chsh_test(circuits)
#test_locally(circuits, True, False, 1)
