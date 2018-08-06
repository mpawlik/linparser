import sys
import os

from numpy import arange
import matplotlib.pyplot as plt
from matplotlib import gridspec

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from linparser.read_logs import read_files, section_on_property, convert_to_list, convert_to_list_difference, \
    print_stats, div1k


def chart_params(ax):
    ax.grid(alpha=0.3)
    ax.set_ylim(0, 5300)
    ax.set_xlim(0, 170)
    ax.xaxis.set_ticks(arange(0, 160, 25))
    ax.yaxis.set_ticks(arange(1000, 5200, 1000))
    ax.tick_params(axis='both', which='both', labelsize='small')
    ax.set_xlabel("Time [s]")
    ax.legend(loc='lower right', fontsize='x-small', )


def first_chart(ax):
    ax.yaxis.set_ticks(arange(0, 5200, 1000))


def absolu(ran):
    mi = min(ran)
    return [i - mi for i in ran]


def gant(master_grid, place, start_data, duration_data, key):
    ax = plt.subplot(master_grid[place])
    count = len(start_data[key])
    ax.barh(range(count), duration_data[key], [1] * count, start_data[key], align='edge', label='%d' % key,
            color=['C%d' % place] * count)
    chart_params(ax)
    return ax


if __name__ == '__main__':
    results = read_files(sys.argv[1:])

    fig = plt.figure(figsize=(14, 10))
    outer = gridspec.GridSpec(3, 1, wspace=0.2, hspace=0.4)

    # AWS
    aws_mem = section_on_property(results['aws'], 'fun_size')

    aws_start = {}
    aws_duration = {}
    for mem in aws_mem.keys():
        tmp = sorted(aws_mem[mem], key=lambda r: r['start'])
        aws_start[mem] = div1k(convert_to_list(tmp, 'start'))
        aws_duration[mem] = div1k(convert_to_list(tmp, 'duration'))
        aws_start[mem] = absolu(aws_start[mem])

        print_stats('aws_start_%d' % mem, aws_start[mem])
        print_stats('aws_duration_%d' % mem, aws_duration[mem])
        print "aws_start_%d after threshold" % mem, len(filter(lambda x: x > 160, aws_start[mem]))

    # GCF
    gcf_mem = section_on_property(results['gcf'], 'fun_size')

    gcf_start = {}
    gcf_duration = {}
    for mem in gcf_mem.keys():
        tmp = sorted(gcf_mem[mem], key=lambda r: r['start'])
        gcf_start[mem] = div1k(convert_to_list(tmp, 'start'))
        gcf_duration[mem] = div1k(convert_to_list(tmp, 'duration'))
        gcf_start[mem] = absolu(gcf_start[mem])

        print_stats('gcf_start_%d' % mem, gcf_start[mem])
        print_stats('gcf_duration_%d' % mem, gcf_duration[mem])
        print "gcf_start_%d after threshold" % mem, len(filter(lambda x: x > 160, gcf_start[mem]))

    # IBM
    ibm_mem = section_on_property(results['ibm'], 'fun_size')

    ibm_start = {}
    ibm_duration = {}
    for mem in ibm_mem.keys():
        tmp = sorted(ibm_mem[mem], key=lambda r: r['start'])
        ibm_start[mem] = div1k(convert_to_list(tmp, 'start'))
        ibm_duration[mem] = div1k(convert_to_list(tmp, 'duration'))
        ibm_start[mem] = absolu(ibm_start[mem])

        print_stats('ibm_start_%d' % mem, ibm_start[mem])
        print_stats('ibm_duration_%d' % mem, ibm_duration[mem])
        print "ibm_start_%d after threshold" % mem, len(filter(lambda x: x > 160, ibm_start[mem]))

    # CHARTS

    aws_c = gridspec.GridSpecFromSubplotSpec(1, 6, subplot_spec=outer[0], wspace=0.)
    gcf_c = gridspec.GridSpecFromSubplotSpec(1, 6, subplot_spec=outer[1], wspace=0.)
    ibm_c = gridspec.GridSpecFromSubplotSpec(1, 6, subplot_spec=outer[2], wspace=0.)

    ax = gant(aws_c, 5, aws_start, aws_duration, 3008)
    ax = gant(aws_c, 4, aws_start, aws_duration, 2048)
    ax = gant(aws_c, 3, aws_start, aws_duration, 1536)
    ax = gant(aws_c, 2, aws_start, aws_duration, 1024)
    ax = gant(aws_c, 1, aws_start, aws_duration, 512)
    ax = gant(aws_c, 0, aws_start, aws_duration, 256)
    first_chart(ax)
    ax.set_ylabel("AWS\nTask id")
    ax = gant(gcf_c, 4, gcf_start, gcf_duration, 2048)
    ax = gant(gcf_c, 3, gcf_start, gcf_duration, 1024)
    ax.set_ylabel("Task id")
    ax = gant(gcf_c, 1, gcf_start, gcf_duration, 512)
    ax = gant(gcf_c, 0, gcf_start, gcf_duration, 256)
    first_chart(ax)
    ax.set_ylabel("GCF\nTask id")
    ax = gant(ibm_c, 1, ibm_start, ibm_duration, 512)
    ax = gant(ibm_c, 0, ibm_start, ibm_duration, 256)
    first_chart(ax)
    ax.set_ylabel("IBM\nTask id")

    # ax = plt.subplot(gs[2])
    # ibm_count = len(ibm_start)
    # ax.barh(range(ibm_count), ibm_duration, [1] * ibm_count, ibm_start, align='edge', color=['C2'] * aws_count)
    # set_params(ax)
    # ax.set_title("IBM")

    plt.gcf().subplots_adjust(right=0.95, left=0.07, top=0.95, bottom=0.7)
    # plt.gcf().subplots_adjust(top=0.25)
    # plt.savefig('gantt.png', dpi=300)
    # plt.savefig('gantt.pdf')
    plt.show()
