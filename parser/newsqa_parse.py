#!/usr/bin/python
import sys, json, csv
import random
from collections import OrderedDict
random.seed(123)

def main():
    res = []
    f = open(sys.argv[1], 'r')
    reader = csv.reader(f)
    header = next(reader)
    rows = [r for r in reader]
    random.shuffle(rows)
    for row in rows:
        if row[3] == '?' or float(row[3]) > 0 or row[4] == '?' or float(row[4]) > 0 or (str(row[5]) == ''):
            continue
        sid = row[0]
        question = row[1]
        ansdict = sorted(eval(row[5]).items(), key=lambda x:x[1], reverse=True)
        if ansdict[0][0] == 'bad_question': continue
        if ansdict[0][0] == 'none': continue
        anspos = map(int, ansdict[0][0].split(':'))
        answer = row[6][anspos[0]:anspos[1]] + ' ({0}:{1})'.format(anspos[0],anspos[1])
        ansdwer = answer.replace('\r', '')
        context = row[6].replace('\r\r\n\r\r\n', '\n').replace('\r\n\r\n','\n').replace('\r', '')
        res.append({'id':'newsqa_{0:03d}'.format(len(res)),
                    'original_id': sid,
                    'contents': {'context': context,
                                 'questions': [{'question':question,
                                                'answer': answer}]}})
        if len(res) >= 100: break
    print 'Extracted (passage,question) pairs:', len(res) # 1152
    return res

if __name__=='__main__':
    res = main()
    with open('newsqa_data.json', 'w') as fp:
        json.dump(res,fp)

