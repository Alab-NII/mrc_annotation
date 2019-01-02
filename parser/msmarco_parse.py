#!/usr/bin/python
import sys, json
import random
from collections import OrderedDict
random.seed(123)
ints_sample = lambda x: sorted(random.sample(range(x), 100))

def main():
    with open(sys.argv[1], 'r') as f:
        jstr = f.readlines()
    data_json = map(json.loads, jstr)
    res = []
    for i in ints_sample(len(data_json)):
        epi = data_json[i]
        qid = epi['query_id']
        answer = ', '.join(epi['answers'])#map(lambda x: '"{0}"'.format(x), epi['answers']))
        qtype = epi['query_type']
        question = epi['query']
        question = question[0].upper() + question[1:] + '?'
        psgs = epi['passages']
        passages = []
        for psg in psgs:
            if psg['is_selected'] == 1:
                passages.append(psg['passage_text'])
        context = '\n'.join(passages)
        res.append({'id':'msmarco_{0:03d}'.format(len(res)), 'oridinal_id': qid, 'contents': {'context': context, 'questions':[{'question':question, 'answer': answer, 'question_type': qtype}]}})
    print 'Extracted (passage,question) pairs:', len(res)
    return res

if __name__=='__main__':
    res = main()
    with open('msmarco_data.json', 'w') as fp:
        json.dump(res,fp)

