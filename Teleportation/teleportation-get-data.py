import numpy as np
import pandas as pd
from check_QE import *

##The date when jobs gathering started, by default the date when teleportation.py was corrected
start_date = '2018-07-10T1'
##Name of a file to save the data in
file_name = 'teleportation_data.csv'

print('Getting done jobs')
jobs = get_done_jobs(0)
jobs = [j for j in jobs if j['creationDate'] > start_date]
print('Number of jobs: ' + str(len(jobs)))

from collections import Counter

print(Counter([j['backend']['name'] for j in jobs]))

print('Parsing data')
data = filter_jobs_data(jobs)
data = pd.DataFrame.from_dict(data)

data['theta'] = np.tile(np.repeat(np.linspace(0, np.pi, 10), 2), int(data.shape[0] / 20))
data['job'] = np.tile(['test', 'teleport'], int(data.shape[0] / 2))
data['index'] = np.repeat(range(int(data.shape[0] / 20)), 20)
data.head()

print('Extracting counts')
results = data.results.apply(pd.Series)
results = results.fillna(0)
results.head()

data['X000'] = results['0000000000000000'] + results['0000000000000100'] + results['00000']
data['X001'] = results['1000000000000000'] + results['1000000000000100'] + results['00100']
data['X010'] = results['0000000000000010'] + results['0000000000000110'] + results['00010']
data['X011'] = results['1000000000000010'] + results['1000000000000110'] + results['00110']
data['X100'] = results['0000000000000001'] + results['0000000000000101'] + results['00001']
data['X101'] = results['1000000000000001'] + results['1000000000000101'] + results['00101']
data['X110'] = results['0000000000000011'] + results['0000000000000111'] + results['00011']
data['X111'] = results['1000000000000011'] + results['1000000000000111'] + results['00111']

print('Computing alpha and beta')
test_data = data.query('job=="test"')
teleport_data = data.query('job=="teleport"')
test_data['alpha'] = test_data.X000 + test_data.X001 + test_data.X010 + test_data.X011
test_data['beta'] = test_data.X100 + test_data.X101 + test_data.X110 + test_data.X111
teleport_data['alpha'] = teleport_data.X000 + teleport_data.X110 + teleport_data.X011 + teleport_data.X101
teleport_data['beta'] = teleport_data.X001 + teleport_data.X111 + teleport_data.X100 + teleport_data.X010

print('Aggragating data')
agg_data = teleport_data[['backend_name', 'date', 'theta', 'index', 'alpha', 'beta']]
agg_data = agg_data.rename(columns={'backend_name': 'backend'})
agg_data['alpha'] = agg_data['alpha'] / 1024
agg_data['beta'] = agg_data['beta'] / 1024
agg_data = agg_data.assign(
    alpha_test=list(test_data.alpha / 1024),
    beta_test=list(test_data.beta / 1024),
    alpha_theory=np.cos(agg_data.theta / 2) ** 2,
    beta_theory=np.sin(agg_data.theta / 2) ** 2
)

agg_data.to_csv(file_name, index=False)

print('Data saved to ' + file_name)
