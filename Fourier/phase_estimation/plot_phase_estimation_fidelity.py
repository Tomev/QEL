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


def plot(array, n, job_base_name, plot_labels=False, save_avg=False, save_plot=False):
    figure, axis = plt.subplots()
    plt.xticks(rotation=45)
    set_axes(axis, n)

    if plot_labels:
        for (j, i), count in np.ndenumerate(array):
            axis.text(i, j, "{:.2f}%".format(100 * count / SHOTS), ha='center', va='center', fontsize=5)

    axis.set_ylabel("Faza bramki")
    axis.set_xlabel("Wynik szacowania")

    if save_avg:
        with open("../../../../Fizyka-licencjat/Pomiary/pe_fidelities.txt", "a") as f:
            f.write("{}\t{}\n".format(job_base_name, 100 * array.trace() / SHOTS / (2 ** n)))

    axis.imshow(array, cmap='viridis')

    if save_plot:
        plt.savefig("../../../../Fizyka-licencjat/Pomiary/X3_{}.pdf".format(job_base_name), transparent=True,
                    bbox_inches='tight', pad_inches=0)

    plt.show()


def main():
    n = 3
    # n = 4
    backend_name = 'ibmq_london'
    # backend_name = 'ibmqx2'
    job_base_name = "pe_fid"
    logical_to_physical = [4, 1, 0, 3]

    backend = get_backend_from_name(backend_name)

    # job = backend.jobs(job_name=re.escape("{}_all".format(job_base_name)))[0]
    # array = make_array([job])

    job = backend.jobs(job_name=re.escape("pe_fid_ltp={}_all".format(logical_to_physical)))[0]
    array = make_array([job], n)

    # job_name_format = "{{}}_{{:0{}b}}".format(n)
    # jobs = [backend.jobs(job_name=job_name_format.format(job_base_name, i))[0] for i in range(8)]
    # array = make_array(jobs)

    # jobs = test_locally_with_noise(get_circuits()[0], backend_name)
    # array = make_array(jobs)

    plot(array, n, job_base_name)


if __name__ == '__main__':
    main()
