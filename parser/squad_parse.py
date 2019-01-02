#!/usr/bin/python
import sys, json
import random
from collections import OrderedDict
random.seed(123)
ints_sample = lambda x: sorted(random.sample(range(x), 100))

def main():
    f = open(sys.argv[1], 'r')
    data_json = json.load(f)
    res = []
    random.shuffle(data_json['data'])
    for epi in data_json['data']:
        title = epi['title']
        paragraphs = epi['paragraphs']
        selected_p_idx = [-1]
        while random.randint(0,10000) % 10 > 0:
            p_idx = -1
            while p_idx in selected_p_idx:
                p_idx = random.randint(0, 10000) % len(paragraphs)
                if len(selected_p_idx) * 10 > len(paragraphs): break
            para = paragraphs[p_idx]
            selected_p_idx.append(p_idx)
            context = para['context']
            qass = para['qas']
            qas = qass[random.randint(0, 10000) % len(qass)]
            question = qas['question']
            answer = ', '.join([x['text'] + ' (' + str(x['answer_start']) + ')' for x in qas['answers']])
            res.append({'id':'squad_{0:03d}'.format(len(res)), 'original_id': qas['id'], 'title': title, 'contents': {'context': context, 'questions': [{'question':question, 'answer': answer}]}})
            if len(res) >= 100:
                break
        if len(res) >= 100:
            break
    print 'Extracted (passage,question) pairs:', len(res)
    return res

if __name__=='__main__':
    res = main()
    with open('squad_data.json', 'w') as fp:
        json.dump(res,fp)

