import sys
sys.path.append('../..')
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import StrMethodFormatter
from run_fidelity_circuits import get_circuits
from methods import test_locally_with_noise, get_backend_from_name
import re
from consts import SHOTS
from Fourier.fourier import archs


parameter_sets = [
    {
        'n': 3,
        'backend_name': 'ibmq_london',
        'job_name': 'F3T_fid_comp_base_ltp=[1, 3, 4]_all'
    },
    {
        'n': 3,
        'backend_name': 'ibmq_london',
        'logical_to_physical': [1, 3, 4]
    },
    {
        'n': 3,
        'backend_name': 'ibmqx2',
        'job_name': 'F3X_fid_comp_base_ltp=[2, 3, 4]_all'
    },
    {
        'n': 3,
        'backend_name': 'ibmqx2',
        'logical_to_physical': [0, 1, 2]
    },
    {
        'n': 4,
        'backend_name': 'ibmq_london',
        'job_name': 'F4T_fid_comp_base_ltp=[0, 1, 3, 4]_all'
    },
    {
        'n': 4,
        'backend_name': 'ibmq_london',
        'logical_to_physical': [0, 1, 3, 4]
    },
    {
        'n': 4,
        'backend_name': 'ibmqx2',
        'job_name': 'F4X_fid_comp_base_ltp=[2, 3, 4, 0]'
    },
    {
        'n': 4,
        'backend_name': 'ibmqx2',
        'logical_to_physical': [2, 0, 1, 3]
    }
]


def set_axes(axis, n):
    for ax in (axis.xaxis, axis.yaxis):
        ax.set_ticks(range(2 ** n))
        ax.set_major_formatter(StrMethodFormatter("{{x:0{}b}}".format(n)))


def permute(x, n, measure_logical_to_physical=None):
    if measure_logical_to_physical is None:
        measure_logical_to_physical = range(n)
    y = 0
    for i in range(n):
        if x & (1 << i):
            y += 1 << (measure_logical_to_physical[i])
    return y


def make_array(jobs, n, measure_logical_to_physical=None):
    dict_key_format = "{{:0{}b}}".format(n)
    counts = []
    if len(jobs) == 1:
        result = jobs[0].result()
        for i in range(2 ** n):
            counts.append(
                [result.get_counts(experiment=i)
                       .get(dict_key_format.format(permute(j, n, measure_logical_to_physical)), 0)
                 for j in range(2 ** n)])
    else:
        results = [job.result() for job in jobs]
        for result in results:
            counts.append([result.get_counts()
                                 .get(dict_key_format.format(permute(j, n, measure_logical_to_physical)), 0)
                           for j in range(2 ** n)])
    return np.array(counts)


def plot(array, n, experiment_name, vmax, plot_labels=False, save_avg=False, save_plot=False):
    figure, axis = plt.subplots()
    plt.xticks(rotation=45)
    set_axes(axis, n)

    if plot_labels:
        for (j, i), count in np.ndenumerate(array):
            axis.text(i, j, "{:.2f}%".format(100 * count / SHOTS), ha='center', va='center', fontsize=5)

    axis.set_ylabel("Faza bramki")
    axis.set_xlabel("Wynik szacowania")

    if save_avg:
        with open("../../../../Fizyka-licencjat/Pomiary/qft_fid.txt", "a") as f:
            f.write("{}\t{}\t{}%\n".format(experiment_name, 100 * array.trace() / SHOTS / (2 ** n), 100 * vmax / SHOTS))

    axis.pcolormesh(np.arange(2 ** n + 1) - 0.5, np.arange(2 ** n + 1) - 0.5, array, cmap='viridis', vmin=0, vmax=vmax)
    axis.axis('image')
    axis.invert_yaxis()

    if save_plot:
        plt.savefig("../../../../Fizyka-licencjat/Pomiary/{}.pdf".format(experiment_name), transparent=True,
                    bbox_inches='tight', pad_inches=0)

    plt.show()


def get_jobs(backend_name, n, job_name=None, logical_to_physical=None, **kwargs):
    backend = get_backend_from_name(backend_name)
    if job_name is not None:
        return [backend.jobs(job_name=re.escape(job_name))[0]]
    else:
        circuits = get_circuits(n, archs[backend_name], backend_name,
                                initial_layout=logical_to_physical)[0]
        return test_locally_with_noise(circuits, backend_name)


def main():
    for parameter_set in parameter_sets:
        n = parameter_set['n']
        backend_name = parameter_set['backend_name']

        jobs = get_jobs(**parameter_set)
        array = make_array(jobs, n, parameter_set.get('measure_logical_to_physical', None))
        vmax = array.max()

        if 'pair' in parameter_set:
            pair_jobs = get_jobs(**parameter_sets[parameter_set['pair']])
            pair_array = make_array(pair_jobs, n, parameter_set.get('measure_logical_to_physical', None))
            vmax = max(vmax, pair_array.max())

        plot(array, n, "qft_fid_{}_n={}_{}".format(backend_name, n, parameter_set.get('job_name', "sim")), vmax=vmax)

    plt.show()


if __name__ == '__main__':
    main()
