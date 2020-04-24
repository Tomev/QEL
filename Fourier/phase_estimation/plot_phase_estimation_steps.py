import sys
sys.path.append('../..')
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import StrMethodFormatter, FuncFormatter
from methods import test_locally_with_noise, get_backend_from_name
import re
from mpl_toolkits.axes_grid1 import host_subplot
from consts import SHOTS


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


def plot(array, n, t, job_base_name, plot_labels=False, save_avg=False, save_plot=False):
    figure = plt.figure()
    axis = host_subplot(1, 1, 1, figure=figure)
    plt.xticks(rotation=45)
    set_axes(axis, n, t)

    if plot_labels:
        for (j, i), count in np.ndenumerate(array):
            axis.text(i, j, "{:.2f}%".format(100 * count / SHOTS), ha='center', va='center', fontsize=5)

    axis.set_ylabel("Miejsce po przecinku")
    axis.set_xlabel("Wartość grupy bitów")

    if save_avg:
        with open("../../../../Fizyka-licencjat/Pomiary/pe_fidelities.txt", "a") as f:
            f.write("{}\t{}\n".format(job_base_name, 100 * array.trace() / SHOTS / (2 ** n)))

    axis.imshow(array, cmap='viridis')

    if save_plot:
        plt.savefig("../../../../Fizyka-licencjat/Pomiary/{}.pdf".format(job_base_name.replace("/", "")),
                    transparent=True, bbox_inches='tight', pad_inches=0)

    plt.show()


def main():
    n = 10
    t = 1
    # t = 2
    # t = 3
    shots = 8192
    # backend_name = 'ibmq_london'
    backend_name = 'ibmqx2'
    job_base_name = "ph_est_pi/4_01_n={}_t={}".format(n, t)

    backend = get_backend_from_name(backend_name)

    # job = backend.jobs(job_name=re.escape("{}_all".format(job_base_name)))[0]
    # array = make_array([job])

    # job = backend.jobs(job_name=re.escape("pe_fid_ltp=[3, 4, 0, 2]_all"))[0]
    # array = make_array([job])

    jobs = [backend.jobs(job_name=re.escape("{}_{}".format(job_base_name, range(max(i - t, 0), i))))[0]
            for i in reversed(range(n, 0, -t))]
    array = make_array(jobs, n, t)

    # jobs = test_locally_with_noise(get_circuits()[0], backend_name)
    # array = make_array(jobs)

    plot(array, n, t, job_base_name)


if __name__ == '__main__':
    main()
