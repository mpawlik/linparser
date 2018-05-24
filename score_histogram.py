import sys
import json
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec, ticker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from linparser.read_logs import read_files, section_on_property, convert_to_list

providers = ['aws', 'gcf', 'ibm']


def set_hist_params(ax):
    ax.grid(alpha=0.3)
    ax.set_ylim(0, 600)
    ax.legend(loc='upper right', fontsize='x-small', )
    ax.xaxis.set_ticks(np.arange(0, 55, 5))
    ax.yaxis.set_ticks(np.arange(0, 600, 200))


def set_scatter_params(ax):
    ax.set_ylim(0, 45)
    ax.set_xlim(0, 2304)
    ax.xaxis.set_ticks([0, 512, 1024, 1536, 2048])
    ax.yaxis.set_ticks(np.arange(0, 45, 5))
    ax.grid(alpha=0.3)
    ax.set_xlabel("Memory size [MB]")
    ax.set_ylabel("Performance [GFlops]")


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

    # gcf_mem_128 = convert_to_list(gcf_mem[128], 'score')
    gcf_mem_256 = convert_to_list(gcf_mem[256], 'score')
    gcf_mem_512 = convert_to_list(gcf_mem[512], 'score')
    gcf_mem_1024 = convert_to_list(gcf_mem[1024], 'score')
    gcf_mem_2048 = convert_to_list(gcf_mem[2048], 'score')

    ibm_mem = section_on_property(results['ibm'], 'fun_size')

    ibm_mem_256 = convert_to_list(ibm_mem[256], 'score')
    ibm_mem_512 = convert_to_list(ibm_mem[512], 'score')

    bins = np.linspace(0, 50, 100)

    fig = plt.figure(figsize=(14, 5))

    outer = gridspec.GridSpec(2, 3, wspace=0.4, hspace=0.3)

    # Scatter >>>>>>>>>>>>>>

    ax = plt.subplot(outer[0])
    ax.scatter(
        [256] * len(aws_mem_256) + [512] * len(aws_mem_512) + [1024] * len(aws_mem_1024) + [1536] * len(
            aws_mem_1536) + [2048] * len(aws_mem_2048),
        aws_mem_256 + aws_mem_512 + aws_mem_1024 + aws_mem_1536 + aws_mem_2048,
        alpha=0.1,
        c=["C0"] * len(aws_mem_256) + ["C1"] * len(aws_mem_512) + ["C2"] * len(aws_mem_1024) + ["C3"] * len(
            aws_mem_1536) + ["C4"] * len(aws_mem_2048)
    )
    ax.set_title("AWS")
    set_scatter_params(ax)

    ax = plt.subplot(outer[1])
    ax.scatter(
        [256] * len(gcf_mem_256) + [512] * len(gcf_mem_512) + [1024] * len(gcf_mem_1024) + [2048] * len(gcf_mem_2048),
        gcf_mem_256 + gcf_mem_512 + gcf_mem_1024 + gcf_mem_2048,
        alpha=0.1,
        c=["C0"] * len(gcf_mem_256) + ["C1"] * len(gcf_mem_512) + ["C2"] * len(gcf_mem_1024) + ["C4"] * len(
            gcf_mem_2048)
    )
    ax.set_title("GCF")
    set_scatter_params(ax)

    ax = plt.subplot(outer[2])
    ax.scatter(
        [256] * len(ibm_mem_256) + [512] * len(ibm_mem_512),
        ibm_mem_256 + ibm_mem_512,
        alpha=0.1,
        c=["C0"] * len(ibm_mem_256) + ["C1"] * len(ibm_mem_512),
    )
    ax.set_title("IBM")
    set_scatter_params(ax)

    # Histograms >>>>>>>>>>>>>>>>

    # AWS

    gs_aws_l = gridspec.GridSpecFromSubplotSpec(5, 1, subplot_spec=outer[3], hspace=.0)

    ax0 = plt.subplot(gs_aws_l[0])
    ax0.hist(aws_mem_256, bins, alpha=0.5, edgecolor='k', label='256', color='C0')
    set_hist_params(ax0)
    ax0.set_ylabel("count")

    ax1 = plt.subplot(gs_aws_l[1])
    ax1.hist(aws_mem_512, bins, alpha=0.5, edgecolor='k', label='512', color='C1')
    set_hist_params(ax1)

    ax2 = plt.subplot(gs_aws_l[2])
    ax2.hist(aws_mem_1024, bins, alpha=0.5, edgecolor='k', label='1024', color='C2')
    set_hist_params(ax2)

    ax3 = plt.subplot(gs_aws_l[3])
    ax3.hist(aws_mem_1536, bins, alpha=0.5, edgecolor='k', label='1536', color='C3')
    set_hist_params(ax3)

    ax4 = plt.subplot(gs_aws_l[4])
    ax4.hist(aws_mem_2048, bins, alpha=0.5, edgecolor='k', label='2048', color='C4')
    set_hist_params(ax4)
    ax4.set_xlabel("Performance [GFlops]")

    # GCF

    gs_gcf_l = gridspec.GridSpecFromSubplotSpec(5, 1, subplot_spec=outer[4], hspace=.0)

    ax0 = plt.subplot(gs_gcf_l[0])
    ax0.hist(gcf_mem_256, bins, alpha=0.5, edgecolor='k', label='256', color='C0')
    set_hist_params(ax0)
    ax0.set_ylabel("count")

    ax1 = plt.subplot(gs_gcf_l[1])
    ax1.hist(gcf_mem_512, bins, alpha=0.5, edgecolor='k', label='512', color='C1')
    set_hist_params(ax1)

    ax2 = plt.subplot(gs_gcf_l[2])
    ax2.hist(gcf_mem_1024, bins, alpha=0.5, edgecolor='k', label='1024', color='C2')
    set_hist_params(ax2)

    ax4 = plt.subplot(gs_gcf_l[4])
    ax4.hist(gcf_mem_2048, bins, alpha=0.5, edgecolor='k', label='2048', color='C4')
    set_hist_params(ax4)
    ax4.set_xlabel("Performance [GFlops]")

    gs_ibm_l = gridspec.GridSpecFromSubplotSpec(5, 1, subplot_spec=outer[5], hspace=.0)

    ax0 = plt.subplot(gs_ibm_l[0])
    ax0.hist(ibm_mem_256, bins, alpha=0.5, edgecolor='k', label='256', color='C0')
    set_hist_params(ax0)
    ax0.set_ylabel("count")

    ax1 = plt.subplot(gs_ibm_l[1])
    ax1.hist(ibm_mem_256, bins, alpha=0.5, edgecolor='k', label='512', color='C1')
    set_hist_params(ax1)
    ax1.set_xlabel("Performance [GFlops]")

    # plt.subplots_adjust(hspace=.0)
    fig.subplots_adjust(top=0.95)
    plt.savefig('score.png', dpi=300)
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
