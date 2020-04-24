import sys
sys.path.append('../..')
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import StrMethodFormatter, FuncFormatter
from methods import test_locally_with_noise, get_backend_from_name
import re
from mpl_toolkits.axes_grid1 import host_subplot
from consts import SHOTS


parameter_sets = [
    {
        'n': 4,
        't': 1,
        'backend_name': 'ibmq_london',
        'job_base_name': 'ph_est_1011_01_n=4_t=1'
    },
    {
        'n': 4,
        't': 1,
        'backend_name': 'ibmqx2',
        'job_base_name': 'ph_est_1011_01_n=4_t=1'
    },
    {
        'n': 4,
        't': 2,
        'backend_name': 'ibmq_london',
        'job_base_name': 'ph_est_1011_134_n=4_t=2'
    },
    {
        'n': 4,
        't': 2,
        'backend_name': 'ibmqx2',
        'job_base_name': 'ph_est_1011_012_n=4_t=2'
    },
    {
        'n': 10,
        't': 1,
        'backend_name': 'ibmq_london',
        'job_base_name': 'ph_est_pi/4_n=10_t=1'
    },
    {
        'n': 10,
        't': 1,
        'backend_name': 'ibmqx2',
        'job_base_name': 'ph_est_pi/4_01_n=10_t=1'
    },
    {
        'n': 10,
        't': 2,
        'backend_name': 'ibmq_london',
        'job_base_name': 'ph_est_pi/4_134_n=10_t=2'
    },
    {
        'n': 10,
        't': 2,
        'backend_name': 'ibmqx2',
        'job_base_name': 'ph_est_pi/4_012_n=10_t=2'
    },
    {
        'n': 10,
        't': 3,
        'backend_name': 'ibmq_london',
        'job_base_name': 'ph_est_pi/4_0134_n=10_t=3'
    },
]


def set_axes(axis, n, t):
    axis.yaxis.set_ticks(range(n))
    axis.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: "{}".format(x + 1)))
    axis.xaxis.set_ticks(range(2 ** t))
    axis.xaxis.set_major_formatter(StrMethodFormatter("{{x:0{}b}}".format(t)))
    if n % t:
        sec_xaxis = axis.twin()
        sec_xaxis.xaxis.set_ticks(np.arange((2 ** ((-n) % t) - 1) / 2, 2 ** t, 2 ** ((-n) % t)))
        sec_xaxis.xaxis.set_major_formatter(
            FuncFormatter(
                lambda x, pos: "{{:0{}b}}".format(n % t).format(pos)))


def make_array(jobs, n, t):
    dict_key_format_format = "{{:0{}b}}"
    counts = []
    results = [job.result() for job in jobs]
    for i, result in zip(reversed(range(n, 0, -t)), results):
        k = min(i, t)
        dict_key_format = dict_key_format_format.format(k)
        for _ in range(min(i, t)):
            counts.append([result.get_counts()[dict_key_format.format(j)[::-1]]
                           for j in range(2 ** k) for _ in range(2 ** (t - k))])
    return np.array(counts)


def plot(array, n, t, experiment_name, plot_labels=False, save_val=False, save_plot=False):
    figure = plt.figure()
    axis = host_subplot(1, 1, 1, figure=figure)
    plt.xticks(rotation=45)
    set_axes(axis, n, t)

    if plot_labels:
        for (j, i), count in np.ndenumerate(array):
            axis.text(i, j, "{:.2f}%".format(100 * count / SHOTS), ha='center', va='center', fontsize=5)

    axis.set_ylabel("Miejsce po przecinku")
    axis.set_xlabel("Wartość grupy bitów")

    if save_val:
        bits = ""
        for i in reversed(range(n, 0, -t)):
            bits += "{{:0{}b}}".format(min(i, t)).format(array[i - 1][::2 ** (max(t - i, 0))].argmax())
        with open("../../../../Fizyka-licencjat/Pomiary/pe_steps.txt", "a") as f:
            f.write("{}\t{}\n".format(experiment_name, bits))

    axis.imshow(array, cmap='viridis')

    if save_plot:
        plt.savefig("../../../../Fizyka-licencjat/Pomiary/{}.pdf".format(experiment_name.replace("/", "")),
                    transparent=True, bbox_inches='tight', pad_inches=0)

    plt.show()


def main():
    for parameter_set in parameter_sets:
        n = parameter_set['n']
        t = parameter_set['t']
        backend_name = parameter_set['backend_name']
        job_base_name = parameter_set['job_base_name']

        backend = get_backend_from_name(backend_name)
        jobs = [backend.jobs(job_name=re.escape("{}_{}".format(job_base_name, range(max(i - t, 0), i))))[0]
                for i in reversed(range(n, 0, -t))]

        array = make_array(jobs, n, t)

        plot(array, n, t, "pe_steps_{}_n={}_t={}_{}".format(backend_name, n, t, job_base_name).replace("/", ""))


if __name__ == '__main__':
    main()
