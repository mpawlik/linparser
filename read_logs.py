import sys
import json
import os


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
            if 'message' in data.keys():
                print "Message: %s" % data['message']
                continue

            data['score'] = extract_performance(data['stdout'])
            data['fun_size'] = extract_fun_size(data['executor_url'])
            data['prob_size'] = extract_prob_size(data['args'])
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


def extract_fun_size(url):
    suffix= url[-6:]
    split_char = '-'
    if '_' in suffix:
        split_char = '_'
    suffix = suffix.split(split_char)[1]

    return int(suffix)


def extract_prob_size(args):
    size = int(args[1][9:].split('.')[0])
    return size


if __name__ == '__main__':
    results = {}
    for inp in sys.argv[1:]:
        provider = os.path.basename(inp).split('_')[0]
        print provider
        results[provider] = process(inp, provider)

    for p in results.keys():
        for r in results[p]:
            print r['score'], r['duration']