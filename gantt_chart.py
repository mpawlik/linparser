import sys
import os

from numpy import arange
import matplotlib.pyplot as plt
from matplotlib import gridspec

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from linparser.read_logs import read_files, section_on_property, convert_to_list, convert_to_list_difference, \
    print_stats, div1k, fix_long


def chart_params(ax):
    ax.grid(alpha=0.3)
    ax.set_ylim(0, 45)
    ax.set_xlim(0, 75)
    ax.xaxis.set_ticks(arange(0, 100, 25))
    ax.yaxis.set_ticks(arange(0, 50, 10))
    ax.tick_params(axis='both', which='both', labelsize='small')
    ax.set_ylabel("Task id")
    ax.set_xlabel("Time [s]")
    ax.legend(loc='lower right', fontsize='xx-small', )


def absolu(ran):
    mi = min(ran)
    return [i - mi for i in ran]


def gant(master_grid, place, start_data, duration_data, name, key):
    ax = plt.subplot(master_grid[place])
    count = len(start_data[key])
    color_map = {
        u'mProjectPP': 'C0',
        u'mDiffFit': 'C1',
        u'mConcatFit': 'C2',
        u'mBgModel': 'C3',
        u'mBackground': 'C4',
        u'mImgtbl': 'C5',
        u'mAdd': 'C6',
        u'mShrink': 'C7',
        u'mJPEG': 'C8'
    }
    colors = map(color_map.get, name[key])

    present_types = []
    for i in range(count):
        if name[key][i] not in present_types:
            ax.barh(i, duration_data[key][i], 1, start_data[key][i], align='edge', label=name[key][i],
                    color=color_map.get(name[key][i]))
            present_types += [name[key][i]]
        else:
            ax.barh(i, duration_data[key][i], 1, start_data[key][i], align='edge',
                    color=color_map.get(name[key][i]))
    chart_params(ax)
    return ax


if __name__ == '__main__':
    results = read_files(sys.argv[1:])

    fig = plt.figure(figsize=(7, 4))
    grid = gridspec.GridSpec(1, 2, wspace=0.4, hspace=0.1)

    fix_long(results)

    start = {}
    duration = {}
    end = {}
    name = {}
    for k in ['pure', 'hybrid']:
        # tmp = sorted(results[k], key=lambda r: r['start'])
        tmp = results[k]
        start[k] = div1k(convert_to_list(tmp, 'start'))
        duration[k] = div1k(convert_to_list(tmp, 'duration'))
        start[k] = absolu(start[k])
        end[k] = div1k(convert_to_list(tmp, 'end'))
        end[k] = absolu(end[k])
        name[k] = convert_to_list(tmp, 'executable')

        print_stats('start_%s' % k, start[k])
        print_stats('duration_%s' % k, duration[k])
        print_stats('end_%s' % k, end[k])

    # CHARTS

    ax = gant(grid, 0, start, duration, name, 'pure')
    ax.set_title("ECS execution")
    ax = gant(grid, 1, start, duration, name, 'hybrid')
    ax.set_title("Hybrid execution")

    # plt.gcf().subplots_adjust(right=0.95, left=0.07, top=0.96, bottom=0.07)
    plt.gcf().subplots_adjust(top=0.90)
    plt.savefig('gantt.png', dpi=300)
    plt.savefig('gantt.pdf')
    plt.show()
