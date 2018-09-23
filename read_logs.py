import sys
import json
import os
from numpy import average, std


def process(filename, provider):
    f = open(filename)
    out = []
    for line in f.readlines():
        if line.startswith("#DATA"):
            if 'html' in line or 'Response not yet ready' in line:
                print "server error"
                print line
                continue
            data = json.loads(line[6:])
            # if 'message' in data.keys():
                # print "Message: %s" % data['message']
                # continue

            # data['score'] = extract_performance(data['stdout'])
            # data['fun_size'] = extract_fun_size(data['executor_url'])
            # data['prob_size'] = extract_prob_size(data['args'])
            data['provider'] = provider
            out += [data]
    return out


def extract_performance(output):
    lines = output.split('\n')
    for l in lines:
        if 'Residual checks PASSED' in l:
            score_line = lines[lines.index(l) - 2]
            return float(score_line.split()[4])
    return -1


# def extract_fun_size(url):
#     suffix = url[-6:]
#     split_char = '-'
#     if '_' in suffix:
#         split_char = '_'
#     suffix = suffix.split(split_char)[1]
#
#     return int(suffix)


# def extract_prob_size(args):
#     size = int(args[1][9:].split('.')[0])
#     return size


def div1k(data):
    return [int(i) / 1000. for i in data]


def read_files(files):
    read_results = {}
    for inp in files:
        provider = os.path.basename(inp).split('.')[0]
        read_results[provider] = process(inp, provider)

    return read_results


def section_on_property(results, key):
    output = {}
    for r in results:
        value = r[key]
        if value in output.keys():
            output[value] += [r]
        else:
            output[value] = [r]

    return output


def print_stats(prov, data):
    print "max(%s): %.2f" % (prov, max(data))
    print "min(%s): %.2f" % (prov, min(data))
    print "avg(%s): %.2f" % (prov, average(data))
    print "std(%s): %.2f" % (prov, std(data))
    print "count(%s): %d" % (prov, len(data))

def fix_long(raw_data):
    for k in raw_data.keys():
        data = raw_data[k]
        adjust = 0
        for d in data:
            duration = int(d['duration'])
            d['start'] = int(d['start']) - adjust
            if duration > 7000:
                print "Adjusting long execution for %s" % d['executable']
                adjust += duration * 0.9
                d['duration'] = duration * 0.1
            d['end'] = int(d['end']) - adjust


def convert_to_list(results, key):
    output = []
    for r in results:
        output += [r[key]]

    return output


def convert_to_list_difference(results, key1, key2):
    output = []
    for r in results:
        output += [r[key1] - r[key2]]

    return output


if __name__ == '__main__':
    results = read_files(sys.argv[1:])
    for p in results.keys():
        for r in results[p]:
            print r['score'], r['duration']
