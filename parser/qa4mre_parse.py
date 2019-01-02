#!/usr/bin/python
import sys, json
import random
from collections import OrderedDict
import xml.etree.ElementTree as etree
random.seed(123)
ints_sample = lambda x: sorted(random.sample(range(x), 100))

"""
usage:
$ python qa4mre_parse.py QA4MRE-2013-EN_GS.xml

data:
http://nlp.uned.es/clef-qa/repository/pastCampaigns.php
Repository > QA4MRE > 2013 > Main_Task > Training_Data > Goldstandard > QA4MRE-2013-EN_GS.xml

questions:
topic = 4
reading-test = 4 per topic
question = 15 per reading-test
"""

def main():
    res = []
    qlist = ints_sample(284)
    print qlist
    qcount = 0
    appcount = 0
    raw_data = etree.parse(sys.argv[1])
    elms = raw_data.getroot()
    for topic in elms.findall('topic'):
        topic_attrib = topic.attrib
        topic_id = topic_attrib['t_id'] + '_' + topic_attrib['t_name']
        for rtest in topic.findall('reading-test'):
            rtest_id = rtest.attrib['r_id']
            context = rtest.find('doc').text.replace("\u2019", "'")
            qs = rtest.findall('q')
            questions = []
            for q in qs:
                if not qcount in qlist:
                    qcount += 1
                    continue
                qcount += 1
                question = q.find('q_str').text
                # print question
                # exit(1)
                cands = []
                for a in q.findall('answer'):
                    tmp = ''
                    if 'correct' in a.attrib.keys():
                        tmp += '*'
                    tmp += a.attrib['a_id'] + ')'
                    tmp += a.text + '\n'
                    cands.append(tmp)
                answer = ' '.join(cands).replace('\u2019', "'")
                questions.append({'question': question, 'answer': answer})
                appcount += 1
            res.append({'id':'qa4mre_{0:03d}'.format(len(res)),
                        'original_id': '{0}_{1}'.format(topic_id, rtest_id),
                        'contents': {'context': context, 'questions': questions}})
    print 'Extracted (passage,question) pairs:', appcount
    return res

if __name__=='__main__':
    res = main()
    with open('qa4mre_data.json', 'w') as fp:
        json.dump(res,fp)

