import sys
sys.path.append('../../..')
from CHSH.CHSH import get_chsh_circuits
from Mermin.mermin_test import get_mermin_circuits

experiments_circuits = get_chsh_circuits()
#experiments_circuits = get_mermin_circuits()

circuit_to_draw = experiments_circuits[0]

plot = circuit_to_draw.draw(output='mpl')
plot.show()

print("Done")
