import sys
import json
import os

from numpy import arange
import matplotlib.pyplot as plt
from matplotlib import gridspec, ticker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from linparser.read_logs import read_files, section_on_property, convert_to_list, convert_to_list_difference

providers = ['aws', 'gcf', 'ibm']


def set_params(ax):
    ax.grid(alpha=0.3)
    ax.set_ylim(0, 5200)
    ax.set_xlim(0, 160)
    ax.xaxis.set_ticks(arange(0, 160, 25))
    ax.yaxis.set_ticks(arange(0, 5200, 500))
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Task id")


def divide(ran):
    return [i / 1000. for i in ran]


def absolu(ran):
    mi = min(ran)
    return [i - mi for i in ran]


if __name__ == '__main__':
    results = read_files(sys.argv[1:])
    # for p in results.keys():
    #     for r in results[p]:
    #         print r['score'], r['duration']

    threshold = 160

    # AWS
    aws_mem = section_on_property(results['aws'], 'fun_size')

    aws_mem[512].sort(key=lambda r: r['start'])
    aws_start = divide(convert_to_list(aws_mem[512], 'start'))
    aws_duration = divide(convert_to_list(aws_mem[512], 'duration'))

    aws_start = absolu(aws_start)

    print "max(aws_duration)", max(aws_duration)
    print "max(aws_start)", max(aws_start)
    print "aws_start after threshold", len(filter(lambda x: x > 160, aws_start))

    # GCF
    gcf_mem = section_on_property(results['gcf'], 'fun_size')

    gcf_mem[512].sort(key=lambda r: r['start'])
    gcf_start = divide(convert_to_list(gcf_mem[512], 'start'))
    gcf_duration = divide(convert_to_list(gcf_mem[512], 'duration'))

    gcf_start = absolu(gcf_start)

    print "max(gcf_duration)", max(gcf_duration)
    print "max(gcf_start)", max(gcf_start)
    print "gcf_start after threshold", len(filter(lambda x: x > 160, gcf_start))

    # IBM
    ibm_mem = section_on_property(results['ibm'], 'fun_size')

    ibm_mem[512].sort(key=lambda r: r['start'])
    ibm_start = divide(convert_to_list(ibm_mem[512], 'start'))
    ibm_duration = divide(convert_to_list(ibm_mem[512], 'duration'))

    ibm_start = absolu(ibm_start)

    print "max(ibm512_duration)", max(ibm_duration)
    print "max(ibm512_start)", max(ibm_start)
    print "ibm_start after threshold", len(filter(lambda x: x > 125, ibm_start))

    fig = plt.figure(figsize=(10, 5))

    gs = gridspec.GridSpec(1, 3, wspace=0.5)

    ax = plt.subplot(gs[0])
    aws_count = len(aws_start)
    ax.barh(range(aws_count), aws_duration, [1] * aws_count, aws_start, align='edge', color=['C0'] * aws_count)
    set_params(ax)
    ax.set_title("AWS")

    ax = plt.subplot(gs[1])
    gcf_count = len(gcf_start)
    ax.barh(range(gcf_count), gcf_duration, [1] * gcf_count, gcf_start, align='edge', color=['C1'] * aws_count)
    set_params(ax)
    ax.set_title("GCF")

    ax = plt.subplot(gs[2])
    ibm_count = len(ibm_start)
    ax.barh(range(ibm_count), ibm_duration, [1] * ibm_count, ibm_start, align='edge', color=['C2'] * aws_count)
    set_params(ax)
    ax.set_title("IBM")

    plt.savefig('gantt.png', dpi=300)
    plt.show()
