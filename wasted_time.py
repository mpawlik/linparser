import sys
import json
import os

from numpy import arange, linspace, average, std
import matplotlib.pyplot as plt
from matplotlib import gridspec, ticker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from linparser.read_logs import read_files, section_on_property, convert_to_list, convert_to_list_difference, \
    print_stats

providers = ['aws', 'gcf', 'ibm']


def set_hist_params(ax):
    # ax.set_yscale('log')
    ax.grid(alpha=0.3)
    ax.set_ylim(0, 300)
    ax.set_xlim(0, 100)
    ax.xaxis.set_ticks(arange(0, 100, 25))
    # ax.yaxis.set_ticks(arange(0, 1000, 200))
    ax.set_xlabel("Time [ms]")
    ax.set_ylabel("count")


def divi(vals):
    return map(lambda x: x % 100, vals)


if __name__ == '__main__':
    results = read_files(sys.argv[1:])
    # for p in results.keys():
    #     for r in results[p]:
    #         print r['score'], r['duration']

    threshold = 5000

    # TODO SPRAWDZIC INNE KONFIGURACJE, SA CIEKAWE, AWS MALY

    # AWS
    aws_mem = section_on_property(results['aws'], 'fun_size')
    aws512 = sorted(aws_mem[512], key=lambda x: x['start'])[:threshold]

    aws_del = convert_to_list(aws512, 'duration')
    aws_del = divi(aws_del)

    print_stats('aws', aws_del)

    # GCF
    gcf_mem = section_on_property(results['gcf'], 'fun_size')
    gcf512 = sorted(gcf_mem[512], key=lambda x: x['start'])[:threshold]

    gcf_del = convert_to_list(gcf512, 'duration')
    gcf_del = divi(gcf_del)

    print_stats('gcf', gcf_del)

    # IBM
    ibm_mem = section_on_property(results['ibm'], 'fun_size')
    ibm512 = sorted(ibm_mem[512], key=lambda x: x['start'])[:threshold]

    ibm_del = convert_to_list(ibm512, 'duration')
    ibm_del = divi(ibm_del)

    print_stats('ibm', ibm_del)

    bins = linspace(0, 100, 50)

    fig = plt.figure(figsize=(15, 4))

    outer = gridspec.GridSpec(1, 3, wspace=0.5, hspace=0.3)

    # aws_del = [i / 1000. for i in aws_del]
    # gcf_del = [i / 1000. for i in gcf_del]
    # ibm_del = [i / 1000. for i in ibm_del]

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
    plt.savefig('wasted_time.png', dpi=300)
    plt.show()
