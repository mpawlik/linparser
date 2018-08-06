import sys
import json
import os

from numpy import arange, linspace, average, std
import matplotlib.pyplot as plt
from matplotlib import gridspec, ticker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from linparser.read_logs import read_files, section_on_property, convert_to_list, convert_to_list_difference, \
    print_stats


def set_hist_params(ax):
    ax.grid(alpha=0.3)
    ax.set_ylim(0, 500)
    ax.set_xlim(0, 100)
    ax.xaxis.set_ticks(arange(25, 100, 25))
    ax.yaxis.set_ticks([0, 200, 400])
    ax.legend(loc='upper right', fontsize='x-small', )


def bottom_hist(ax):
    ax.xaxis.set_ticks(arange(0, 125, 25))
    ax.set_xlabel("Time [ms]")


def divi(vals):
    return map(lambda x: x % 100, vals)


def histo(master_grid, place, key, data, bins):
    ax = plt.subplot(master_grid[place])
    ax.hist(data[key], bins, alpha=0.5, edgecolor='k', label='%d' % key, color='C%d' % place)
    set_hist_params(ax)
    return ax


if __name__ == '__main__':
    results = read_files(sys.argv[1:])

    fig = plt.figure(figsize=(14, 5))
    outer = gridspec.GridSpec(1, 3, wspace=0.4, hspace=0.3)

    threshold = 5000

    # AWS
    aws_mem = section_on_property(results['aws'], 'fun_size')
    aws_was = {}
    for mem in aws_mem.keys():
        tmp = sorted(aws_mem[mem], key=lambda x: x['start'])[:threshold]
        aws_was[mem] = divi(convert_to_list(tmp, 'duration'))

    for i in aws_was.keys():
        print_stats('aws%d' % i, aws_was[i])

    # GCF
    gcf_mem = section_on_property(results['gcf'], 'fun_size')
    gcf_was = {}
    for mem in gcf_mem.keys():
        tmp = sorted(gcf_mem[mem], key=lambda x: x['start'])[:threshold]
        gcf_was[mem] = divi(convert_to_list(tmp, 'duration'))

    for i in gcf_was.keys():
        print_stats('gcf%d' % i, gcf_was[i])

    # IBM
    ibm_mem = section_on_property(results['ibm'], 'fun_size')
    ibm_was = {}
    for mem in ibm_mem.keys():
        tmp = sorted(ibm_mem[mem], key=lambda x: x['start'])[:threshold]
        ibm_was[mem] = divi(convert_to_list(tmp, 'duration'))

    for i in ibm_was.keys():
        print_stats('ibm%d' % i, ibm_was[i])

    bins = linspace(0, 100, 50)

    aws_c = gridspec.GridSpecFromSubplotSpec(6, 1, subplot_spec=outer[0], hspace=.0)
    gcf_c = gridspec.GridSpecFromSubplotSpec(6, 1, subplot_spec=outer[1], hspace=.0)
    ibm_c = gridspec.GridSpecFromSubplotSpec(6, 1, subplot_spec=outer[2], hspace=.0)

    ax = histo(aws_c, 0, 256, aws_was, bins)
    ax.set_title("AWS")
    ax = histo(aws_c, 1, 512, aws_was, bins)
    ax.set_ylabel("Count")
    ax = histo(aws_c, 2, 1024, aws_was, bins)
    ax = histo(aws_c, 3, 1536, aws_was, bins)
    ax = histo(aws_c, 4, 2048, aws_was, bins)
    ax = histo(aws_c, 5, 3008, aws_was, bins)
    bottom_hist(ax)

    ax = histo(gcf_c, 0, 256, gcf_was, bins)
    ax.set_title("GCF")
    ax = histo(gcf_c, 1, 512, gcf_was, bins)
    ax.set_ylabel("Count")
    ax = histo(gcf_c, 2, 1024, gcf_was, bins)
    bottom_hist(ax)
    ax = histo(gcf_c, 4, 2048, gcf_was, bins)
    bottom_hist(ax)

    ax = histo(ibm_c, 0, 256, ibm_was, bins)
    ax.set_title("IBM")
    ax = histo(ibm_c, 1, 512, ibm_was, bins)
    ax.set_ylabel("Count")
    bottom_hist(ax)

    plt.savefig('wasted_time.png', dpi=300)
    plt.show()
