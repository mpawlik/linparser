import sys
import json


def process(filename):
    f = open(filename)
    out = []
    for line in f.readlines():
        if line.startswith("#DATA"):
            data = json.loads(line[6:])
            data['score'] = extract_performance(data['stdout'])
            out += [data]
    return out


def extract_performance(output):
    lines = output.split('\n')
    for l in lines:
        if 'Residual checks PASSED' in l:
            score_line = lines[lines.index(l) - 2]
            return float(score_line.split()[4])
    return -1


if __name__ == '__main__':
    results = process(sys.argv[1])
    print results[0].keys()
    for r in results:
        print r['duration'], r['score']
