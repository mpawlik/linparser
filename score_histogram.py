import sys
import json
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec, ticker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from linparser.read_logs import read_files, section_on_property, convert_to_list

providers = ['aws', 'gcf', 'ibm']


def set_params(ax):

    ax.grid(alpha=0.3)
    ax.set_ylim(0, 150)
    ax.legend(loc='upper right')
    ax.xaxis.set_ticks(np.arange(0, 55, 5))
    ax.yaxis.set_ticks(np.arange(0, 150, 50))
    ax.set_ylabel("count")


if __name__ == '__main__':
    results = read_files(sys.argv[1:])
    # for p in results.keys():
    #     for r in results[p]:
    #         print r['score'], r['duration']

    aws_mem = section_on_property(results['aws'], 'fun_size')

    aws_mem_256 = convert_to_list(aws_mem[256], 'score')
    aws_mem_512 = convert_to_list(aws_mem[512], 'score')
    aws_mem_1024 = convert_to_list(aws_mem[1024], 'score')
    aws_mem_1536 = convert_to_list(aws_mem[1536], 'score')
    aws_mem_2048 = convert_to_list(aws_mem[2048], 'score')

    gcf_mem = section_on_property(results['gcf'], 'fun_size')

    gcf_mem_128 = convert_to_list(gcf_mem[128], 'score')
    gcf_mem_256 = convert_to_list(gcf_mem[256], 'score')
    gcf_mem_512 = convert_to_list(gcf_mem[512], 'score')
    gcf_mem_1024 = convert_to_list(gcf_mem[1024], 'score')
    gcf_mem_2048 = convert_to_list(gcf_mem[2048], 'score')

    ibm_mem = section_on_property(results['ibm'], 'fun_size')

    ibm_mem_256 = convert_to_list(ibm_mem[256], 'score')
    ibm_mem_512 = convert_to_list(ibm_mem[512], 'score')

    bins = np.linspace(0, 50, 100)

    fig = plt.figure()
    gs = gridspec.GridSpec(5, 1)



    ax0 = plt.subplot(gs[0])
    ax0.hist(aws_mem_256, bins, alpha=0.5, edgecolor='k', label='256', color='C0')
    set_params(ax0)

    ax1 = plt.subplot(gs[1])
    ax1.hist(aws_mem_512, bins, alpha=0.5, edgecolor='k', label='512', color='C1')
    set_params(ax1)

    ax2 = plt.subplot(gs[2])
    ax2.hist(aws_mem_1024, bins, alpha=0.5, edgecolor='k', label='1024', color='C2')
    set_params(ax2)

    ax3 = plt.subplot(gs[3])
    ax3.hist(aws_mem_1536, bins, alpha=0.5, edgecolor='k', label='1536', color='C3')
    set_params(ax3)

    ax4 = plt.subplot(gs[4])
    ax4.hist(aws_mem_2048, bins, alpha=0.5, edgecolor='k', label='2048', color='C4')
    set_params(ax4)

    plt.subplots_adjust(hspace=.0)
    plt.suptitle('AWS')
    plt.xlabel("GFlops")
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
