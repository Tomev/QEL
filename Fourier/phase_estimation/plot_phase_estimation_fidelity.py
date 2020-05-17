import sys
sys.path.append('../..')
from qiskit import IBMQ
from Qconfig import APItoken
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import StrMethodFormatter
from run_phase_estimation_fidelity import get_circuits
from methods import test_locally_with_noise, get_backend_from_name
import re
from consts import SHOTS


parameter_sets = [
    {
        'n': 3,
        'backend_name': 'ibmq_london',
        'job_name': 'pe_fid_ltp=[4, 1, 0, 3]_all',
        'pair': 1
    },
    {
        'n': 3,
        'backend_name': 'ibmqx2',
        'job_name': 'pe_fid_ltp=[3, 4, 0, 2]_all',
        'pair': 0
    },
    {
        'n': 4,
        'backend_name': 'ibmq_london',
        'job_name': 'pe_fid_ltp=[3, 1, 0, 2, 4]_all'
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
                [result.get_counts(experiment=i)[
                     dict_key_format.format(permute(j, n, measure_logical_to_physical))[::-1]]
                 for j in range(2 ** n)])
    else:
        results = [job.result() for job in jobs]
        for result in results:
            counts.append([result.get_counts()[dict_key_format.format(permute(j, n, measure_logical_to_physical))[::-1]]
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
        with open("../../../../Fizyka-licencjat/Pomiary/pe_fid.txt", "a") as f:
            f.write("{}\t{}\t{}%\n".format(experiment_name, 100 * array.trace() / SHOTS / (2 ** n), 100 * vmax / SHOTS))

    axis.pcolormesh(np.arange(2 ** n + 1) - 0.5, np.arange(2 ** n + 1) - 0.5, array, cmap='viridis', vmin=0, vmax=vmax)
    axis.axis('image')
    axis.invert_yaxis()

    if save_plot:
        plt.savefig("../../../../Fizyka-licencjat/Pomiary/{}.pdf".format(experiment_name), transparent=True,
                    bbox_inches='tight', pad_inches=0)

    plt.show()


def get_jobs(backend_name, job_name, **kwargs):
    backend = get_backend_from_name(backend_name)
    return [backend.jobs(job_name=re.escape(job_name))[0]]


def main():
    for parameter_set in parameter_sets:
        n = parameter_set['n']
        backend_name = parameter_set['backend_name']

        jobs = get_jobs(**parameter_set)
        array = make_array(jobs, n)
        vmax = array.max()

        if 'pair' in parameter_set:
            pair_jobs = get_jobs(**parameter_sets[parameter_set['pair']])
            pair_array = make_array(pair_jobs, n)
            vmax = max(vmax, pair_array.max())

        plot(array, n, "pe_fid_{}_n={}_{}".format(backend_name, n, parameter_set['job_name']),
             vmax=vmax)


if __name__ == '__main__':
    main()
