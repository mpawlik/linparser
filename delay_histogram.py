import sys
import json
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec, ticker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from linparser.read_logs import read_files, section_on_property, convert_to_list, convert_to_list_difference

providers = ['aws', 'gcf', 'ibm']


def set_hist_params(ax):
    ax.grid(alpha=0.3)
    ax.set_ylim(0, 900)
    ax.set_xlim(0, 100)
    ax.xaxis.set_ticks(np.arange(0, 100, 30))
    ax.yaxis.set_ticks(np.arange(0, 1000, 200))
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("count")


if __name__ == '__main__':
    results = read_files(sys.argv[1:])
    # for p in results.keys():
    #     for r in results[p]:
    #         print r['score'], r['duration']

    aws_mem = section_on_property(results['aws'], 'fun_size')

    aws_del = convert_to_list_difference(aws_mem[512], 'start', 'request_start')

    gcf_mem = section_on_property(results['gcf'], 'fun_size')

    gcf_del = convert_to_list_difference(gcf_mem[512], 'start', 'request_start')

    ibm_mem = section_on_property(results['ibm'], 'fun_size')

    ibm_del = convert_to_list_difference(ibm_mem[512], 'start', 'request_start')

    bins = np.linspace(0, 100, 50)

    fig = plt.figure(figsize=(15, 5))

    outer = gridspec.GridSpec(1, 3, wspace=0.5, hspace=0.3)

    aws_del = [i / 1000. for i in aws_del]
    gcf_del = [i / 1000. for i in gcf_del]
    ibm_del = [i / 1000. for i in ibm_del]

    # Scatter >>>>>>>>>>>>>>

    ax = plt.subplot(outer[0])
    ax.hist(aws_del, bins, alpha=0.5, edgecolor='k', label='delay', color='C0')
    set_hist_params(ax)
    ax.set_title("AWS")

    ax = plt.subplot(outer[1])
    ax.hist(gcf_del, bins, alpha=0.5, edgecolor='k', label='delay', color='C1')
    set_hist_params(ax)
    ax.set_title("GCF")

    ax = plt.subplot(outer[2])
    ax.hist(ibm_del, bins, alpha=0.5, edgecolor='k', label='delay', color='C2')
    set_hist_params(ax)
    ax.set_title("IBM")

    # AWS

    # gs_aws_l = gridspec.GridSpecFromSubplotSpec(5, 1, subplot_spec=outer[3], hspace=.0)
    #
    # ax0 = plt.subplot(gs_aws_l[0])
    # ax0.hist(aws_mem_256, bins, alpha=0.5, edgecolor='k', label='256', color='C0')
    # set_hist_params(ax0)
    # ax0.set_ylabel("count")

    plt.show()

    # fig, axes = plt.subplots(nrows=1, ncols=3)
    # ax0, ax1, ax2 = axes
    #
    # bins = np.linspace(0, 100, 40)
    # ax0.hist(aws_mem_256, bins, alpha=0.5, edgecolor='k', label='256')
    # ax0.set_title('AWS')
    # ax0.legend(loc='upper right')
    #
    # fig.tight_layout()
    # plt.show()
