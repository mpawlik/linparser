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
    ax.set_yscale('log')
    ax.grid(alpha=0.3)
    ax.set_ylim(1, 10000)
    ax.set_xlim(0, 300)
    ax.xaxis.set_ticks(np.arange(0, 300, 50))
    # ax.yaxis.set_ticks(np.arange(0, 1000, 200))
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("count")


if __name__ == '__main__':
    results = read_files(sys.argv[1:])
    # for p in results.keys():
    #     for r in results[p]:
    #         print r['score'], r['duration']

    aws_mem = section_on_property(results['aws'], 'fun_size')

    aws_del = convert_to_list_difference(aws_mem[512], 'start', 'request_start')

    print "max(aws_del)", max(aws_del)

    gcf_mem = section_on_property(results['gcf'], 'fun_size')

    gcf_del = convert_to_list_difference(gcf_mem[512], 'start', 'request_start')
    print "max(gcf_del)", max(gcf_del)

    ibm_mem = section_on_property(results['ibm'], 'fun_size')

    ibm_del = convert_to_list_difference(ibm_mem[512], 'start', 'request_start')
    print "max(ibm_del)", max(ibm_del)

    bins = np.linspace(0, 300, 50)

    fig = plt.figure(figsize=(15, 2))

    outer = gridspec.GridSpec(1, 3, wspace=0.5, hspace=0.3)

    aws_del = [i / 1000. for i in aws_del]
    gcf_del = [i / 1000. for i in gcf_del]
    ibm_del = [i / 1000. for i in ibm_del]

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

    plt.gcf().subplots_adjust(bottom=0.25)
    plt.savefig('delay.png', dpi=300)
    plt.show()