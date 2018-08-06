import sys
import json
import os

from numpy import arange, linspace, average, std
import matplotlib.pyplot as plt
from matplotlib import gridspec, ticker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from linparser.read_logs import read_files, section_on_property, convert_to_list, convert_to_list_difference, \
    print_stats

# PING TIMES
# AWS: 23.622
# GCF: 13.091 ms
# IBM: 41.265


def set_hist_params(ax):
    ax.set_yscale('log')
    ax.grid(alpha=0.3)
    ax.set_ylim(1, 1500)
    ax.set_xlim(0, 1750)
    ax.xaxis.set_ticks(arange(250, 1750, 250))
    ax.yaxis.set_ticks([1, 10, 100])
    ax.minorticks_off()
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.legend(loc='upper right', fontsize='x-small', )


def bottom_hist(ax):
    ax.xaxis.set_ticks(arange(0, 2000, 250))
    ax.set_xlabel("Time [ms]")


def histo(master_grid, place, key, data, bins):
    ax = plt.subplot(master_grid[place])
    ax.hist(data[key], bins, alpha=0.5, edgecolor='k', label='%d' % key, color='C%d' % place)
    set_hist_params(ax)
    return ax


if __name__ == '__main__':
    results = read_files(sys.argv[1:])

    threshold = 1000

    fig = plt.figure(figsize=(14, 5))
    outer = gridspec.GridSpec(1, 3, wspace=0.4, hspace=0.3)

    # AWS
    aws_mem = section_on_property(results['aws'], 'fun_size')
    aws_over = {}
    for mem in aws_mem.keys():
        tmp = sorted(aws_mem[mem], key=lambda x: x['start'])[:threshold]
        aws_over[mem] = convert_to_list_difference(tmp, 'request_end', 'end')

    for i in aws_over.keys():
        print_stats('aws%d' % i, aws_over[i])

    # GCF
    gcf_mem = section_on_property(results['gcf'], 'fun_size')
    gcf_over = {}
    for mem in gcf_mem.keys():
        tmp = sorted(gcf_mem[mem], key=lambda x: x['start'])[:threshold]
        gcf_over[mem] = convert_to_list_difference(tmp, 'request_end', 'end')

    for i in gcf_over.keys():
        print_stats('gcf%d' % i, gcf_over[i])

    # IBM
    ibm_mem = section_on_property(results['ibm'], 'fun_size')
    ibm_over = {}
    for mem in ibm_mem.keys():
        tmp = sorted(ibm_mem[mem], key=lambda x: x['start'])[:threshold]
        ibm_over[mem] = convert_to_list_difference(tmp, 'request_end', 'end')

    for i in ibm_over.keys():
        print_stats('ibm%d' % i, ibm_over[i])

    bins = linspace(0, 1500, 50)

    aws_c = gridspec.GridSpecFromSubplotSpec(6, 1, subplot_spec=outer[0], hspace=.0)
    gcf_c = gridspec.GridSpecFromSubplotSpec(6, 1, subplot_spec=outer[1], hspace=.0)
    ibm_c = gridspec.GridSpecFromSubplotSpec(6, 1, subplot_spec=outer[2], hspace=.0)

    ax = histo(aws_c, 0, 256, aws_over, bins)
    ax.set_title("AWS")
    ax = histo(aws_c, 1, 512, aws_over, bins)
    ax.set_ylabel("Count, log")
    ax = histo(aws_c, 2, 1024, aws_over, bins)
    ax = histo(aws_c, 3, 1536, aws_over, bins)
    ax = histo(aws_c, 4, 2048, aws_over, bins)
    ax = histo(aws_c, 5, 3008, aws_over, bins)
    bottom_hist(ax)

    ax = histo(gcf_c, 0, 256, gcf_over, bins)
    ax.set_title("GCF")
    ax = histo(gcf_c, 1, 512, gcf_over, bins)
    ax.set_ylabel("Count, log")
    ax = histo(gcf_c, 2, 1024, gcf_over, bins)
    bottom_hist(ax)
    ax = histo(gcf_c, 4, 2048, gcf_over, bins)
    bottom_hist(ax)

    ax = histo(ibm_c, 0, 256, ibm_over, bins)
    ax.set_title("IBM")
    ax = histo(ibm_c, 1, 512, ibm_over, bins)
    ax.set_ylabel("Count, log")
    bottom_hist(ax)

    plt.gcf().subplots_adjust(right=0.95, left=0.07, top=0.9, bottom=0.13)
    plt.savefig('overhead.png', dpi=300)
    plt.savefig('overhead.pdf')
    # plt.show()
