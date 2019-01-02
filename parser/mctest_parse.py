#!/usr/bin/python
import sys, json
import random
from collections import OrderedDict
random.seed(123)
ints_sample = lambda x: sorted(random.sample(range(x), 100/4))

"""
usage:
$ python mctest_parse.py mc160_dev.tsv mc500_dev.tsv mc160.dev.ans mc500.dev.ans
"""

def main():
    res = []
    lines = []
    anslines = []
    with open(sys.argv[1], 'r') as f:
        lines += f.readlines()
    with open(sys.argv[2], 'r') as f:
        lines += f.readlines()
    with open(sys.argv[3], 'r') as f:
        anslines += f.readlines()
    with open(sys.argv[4], 'r') as f:
        anslines += f.readlines()
    print len(lines)
    for i in ints_sample(len(lines)):
        line = lines[i]
        ansline = anslines[i]
        line = line.replace('\\newline', '\n').replace('\r\n', '')
        pas = line.split('\t')
        cid = pas[0]
        header = pas[1]
        context = pas[2]
        qs = []
        anslist = map(lambda x: ord(x.strip())-ord('A'), ansline.split('\t'))
        for i in range(4):
            cands = pas[4+i*5:4+i*5+4]
            qtmp = pas[3+i*5]
            cands = [chr(ord('A')+x) + ')' + c for x, c in enumerate(cands)]
            cands[anslist[i]] = '*' + cands[anslist[i]]
            ansstr = ' \n'.join(cands)
            qs.append({'question': qtmp, 'answer': ansstr})
        res.append({'id':'mctest_{0:03d}'.format(len(res)), 'original_id': cid, 'contents': {'context': context, 'questions': qs}})
    print 'Extracted (passage,question) pairs:', len(res)*4
    return res

if __name__=='__main__':
    res = main()
    with open('mctest_data.json', 'w') as fp:
        json.dump(res,fp)

