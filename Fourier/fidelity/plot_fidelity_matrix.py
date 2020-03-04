import sys
sys.path.append('../..')
from qiskit import IBMQ
from Qconfig import APItoken
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import StrMethodFormatter
from run_fidelity_circuits import get_circuits
from methods import test_locally_with_noise, get_backend_from_name


n = 3
shots = 8192
backend_name = 'ibmqx2'
job_base_name = "F3X_fidelity_computational_base"


def set_axes(axis):
    for ax in (axis.xaxis, axis.yaxis):
        ax.set_ticks(range(2 ** n))
        ax.set_major_formatter(StrMethodFormatter("{{x:0{}b}}".format(n)))


def make_array(jobs):
    dict_key_format = "{{:0{}b}}".format(n)
    counts = []
    if len(jobs) == 1:
        result = jobs[0].result()
        for i in range(2 ** n):
            counts.append([result.get_counts(experiment=i)[dict_key_format.format(j)] for j in range(2 ** n)])
    else:
        results = [job.result() for job in jobs]
        for result in results:
            counts.append([result.get_counts()[dict_key_format.format(j)] for j in range(2 ** n)])
    return np.array(counts)


def main():
    backend = get_backend_from_name(backend_name)

    job = backend.jobs(job_name="{}_all".format(job_base_name))[0]
    array = make_array([job])

    # jobs = [backend.jobs(job_name="{}_{:03b}".format(job_base_name, i))[0] for i in range(8)]
    # array = make_array(jobs)

    # WARNING: this takes the backend from consts.CONSIDERED_REMOTE_BACKENDS
    # jobs = test_locally_with_noise(get_circuits())
    # array = make_array(jobs)

    figure, axis = plt.subplots()
    set_axes(axis)
    for (j, i), count in np.ndenumerate(array):
        axis.text(i, j, "{:.2f}%".format(100 * count / shots), ha='center', va='center')
    axis.imshow(array, cmap='viridis')
    plt.show()


if __name__ == '__main__':
    main()
