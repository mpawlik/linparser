import sys
import json
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec, ticker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from linparser.read_logs import read_files, section_on_property, convert_to_list, convert_to_list_difference, \
    print_stats

providers = ['aws', 'gcf', 'ibm']


def set_hist_params(ax):
    ax.set_yscale('log')
    ax.grid(alpha=0.3)
    ax.set_ylim(1, 10000)
    ax.set_xlim(0, 300)
    ax.xaxis.set_ticks(np.arange(50, 300, 50))
    ax.minorticks_off()
    ax.yaxis.set_ticks([1, 100, 1000])
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.legend(loc='upper right', fontsize='x-small', )

def div1k(data):
    tmp = [i / 1000. for i in data]
    data = tmp
    return data


if __name__ == '__main__':
    results = read_files(sys.argv[1:])

    fig = plt.figure(figsize=(14, 5))
    outer = gridspec.GridSpec(1, 3, wspace=0.4, hspace=0.3)

    aws_mem = section_on_property(results['aws'], 'fun_size')
    aws_del_256 = convert_to_list_difference(aws_mem[256], 'start', 'request_start')
    aws_del_512 = convert_to_list_difference(aws_mem[512], 'start', 'request_start')
    aws_del_1024 = convert_to_list_difference(aws_mem[1024], 'start', 'request_start')
    aws_del_1536 = convert_to_list_difference(aws_mem[1536], 'start', 'request_start')
    aws_del_2048 = convert_to_list_difference(aws_mem[2048], 'start', 'request_start')
    aws_del_3008 = convert_to_list_difference(aws_mem[3008], 'start', 'request_start')

    gcf_mem = section_on_property(results['gcf'], 'fun_size')
    gcf_del_256 = convert_to_list_difference(gcf_mem[256], 'start', 'request_start')
    gcf_del_512 = convert_to_list_difference(gcf_mem[512], 'start', 'request_start')
    gcf_del_1024 = convert_to_list_difference(gcf_mem[1024], 'start', 'request_start')
    gcf_del_2048 = convert_to_list_difference(gcf_mem[2048], 'start', 'request_start')

    ibm_mem = section_on_property(results['ibm'], 'fun_size')
    ibm_del_256 = convert_to_list_difference(ibm_mem[256], 'start', 'request_start')
    ibm_del_512 = convert_to_list_difference(ibm_mem[512], 'start', 'request_start')

    aws_del_256 = div1k(aws_del_256)
    aws_del_512 = div1k(aws_del_512)
    aws_del_1024 = div1k(aws_del_1024)
    aws_del_1536 = div1k(aws_del_1536)
    aws_del_2048 = div1k(aws_del_2048)
    aws_del_3008 = div1k(aws_del_3008)

    gcf_del_256 = div1k(gcf_del_256)
    gcf_del_512 = div1k(gcf_del_512)
    gcf_del_1024 = div1k(gcf_del_1024)
    gcf_del_2048 = div1k(gcf_del_2048)

    ibm_del_256 = div1k(ibm_del_256)
    ibm_del_512 = div1k(ibm_del_512)

    print_stats('aws256', aws_del_256)
    print_stats('aws512', aws_del_512)
    print_stats('aws1024', aws_del_1024)
    print_stats('aws1536', aws_del_1536)
    print_stats('aws2048', aws_del_2048)
    print_stats('aws3008', aws_del_3008)

    print_stats('gcf256', gcf_del_256)
    print_stats('gcf512', gcf_del_512)
    print_stats('gcf1024', gcf_del_1024)
    print_stats('gcf2048', gcf_del_2048)

    print_stats('ibm256', ibm_del_256)
    print_stats('ibm512', ibm_del_512)

    aws_c = gridspec.GridSpecFromSubplotSpec(6, 1, subplot_spec=outer[0], hspace=.0)
    gcf_c = gridspec.GridSpecFromSubplotSpec(6, 1, subplot_spec=outer[1], hspace=.0)
    ibm_c = gridspec.GridSpecFromSubplotSpec(6, 1, subplot_spec=outer[2], hspace=.0)

    bins = np.linspace(0, 300, 50)

    # AWS
    ax = plt.subplot(aws_c[0])
    ax.hist(aws_del_256, bins, alpha=0.5, edgecolor='k', label='256', color='C0')
    set_hist_params(ax)
    ax.set_title("AWS")

    ax = plt.subplot(aws_c[1])
    ax.hist(aws_del_512, bins, alpha=0.5, edgecolor='k', label='512', color='C1')
    set_hist_params(ax)
    ax.set_ylabel("count, log")

    ax = plt.subplot(aws_c[2])
    ax.hist(aws_del_1024, bins, alpha=0.5, edgecolor='k', label='1024', color='C2')
    set_hist_params(ax)

    ax = plt.subplot(aws_c[3])
    ax.hist(aws_del_1536, bins, alpha=0.5, edgecolor='k', label='1536', color='C3')
    set_hist_params(ax)

    ax = plt.subplot(aws_c[4])
    ax.hist(aws_del_2048, bins, alpha=0.5, edgecolor='k', label='2048', color='C4')
    set_hist_params(ax)

    ax = plt.subplot(aws_c[5])
    ax.hist(aws_del_3008, bins, alpha=0.5, edgecolor='k', label='3008', color='C5')
    set_hist_params(ax)
    ax.set_xlabel("Time [s]")
    ax.xaxis.set_ticks(np.arange(0, 300, 50))

    # GCF
    ax = plt.subplot(gcf_c[0])
    ax.hist(gcf_del_256, bins, alpha=0.5, edgecolor='k', label='256', color='C0')
    set_hist_params(ax)
    ax.set_title("GCF")

    ax = plt.subplot(gcf_c[1])
    ax.hist(gcf_del_512, bins, alpha=0.5, edgecolor='k', label='512', color='C1')
    set_hist_params(ax)
    ax.set_ylabel("count, log")

    ax = plt.subplot(gcf_c[2])
    ax.hist(gcf_del_1024, bins, alpha=0.5, edgecolor='k', label='1024', color='C2')
    set_hist_params(ax)
    ax.set_xlabel("Time [s]")
    ax.xaxis.set_ticks(np.arange(0, 300, 50))

    ax = plt.subplot(gcf_c[4])
    ax.hist(gcf_del_2048, bins, alpha=0.5, edgecolor='k', label='2048', color='C4')
    set_hist_params(ax)
    ax.set_xlabel("Time [s]")
    ax.xaxis.set_ticks(np.arange(0, 300, 50))

    # IBM
    ax = plt.subplot(ibm_c[0])
    ax.hist(ibm_del_256, bins, alpha=0.5, edgecolor='k', label='256', color='C0')
    set_hist_params(ax)
    ax.set_title("IBM")

    ax = plt.subplot(ibm_c[1])
    ax.hist(ibm_del_512, bins, alpha=0.5, edgecolor='k', label='512', color='C1')
    set_hist_params(ax)
    ax.set_ylabel("count, log")
    ax.set_xlabel("Time [s]")
    ax.xaxis.set_ticks(np.arange(0, 300, 50))

    # plt.gcf().subplots_adjust(bottom=0.25)
    plt.savefig('delay.png', dpi=300)
    plt.show()
