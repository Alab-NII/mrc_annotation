#!/usr/bin/python
import sys, json
import random
from collections import OrderedDict
import xml.etree.ElementTree as etree
from htmlentitydefs import name2codepoint
random.seed(123)
ints_sample = lambda x: sorted(random.sample(range(x), 100))

# topic: 4
# reading-test: 4 for each topic
# question: 15 for each reading-test

def main():
    res = []
    qlist = ints_sample(284)
    qcount = 0
    appcount = 0
    parser = etree.XMLParser()
    parser.parser.UseForeignDTD(True)
    parser.entity.update((x, unichr(i)) for x, i in name2codepoint.iteritems())
    raw_data = etree.parse(sys.argv[1], parser=parser)
    elms = raw_data.getroot()
    mclist = elms.findall('mc')
    qlist = ints_sample(len(mclist))
    for i in qlist:
        mc = mclist[i]
        qset = mc.find('question')
        mc_id = qset.attrib['id']
        lc = qset.find('leftcontext').text
        bl = qset.find('blank')
        rc = qset.find('rightcontext').text
        question = (lc.strip() if lc else "") + ' _____ ' + (rc.strip() if rc else "")
        qtype = bl.attrib['type']
        context = mc.find('contextart').text.strip()
        cands = []
        for cand in  mc.findall('choice'):
            cand_id = cand.attrib['idx']
            cand_cor = cand.attrib['correct']
            cand_stat = cand.text.strip()
            cand_str = "{0}) {1}".format(cand_id, cand_stat)
            if cand_cor == "true":
                cand_str = "*" + cand_str
            cands.append(cand_str)
        answer = "\n".join(cands)
        questions = [{'question': question, 'answer': answer, 'question_type': qtype}]
        res.append({'id':'wdw_{0:03d}'.format(len(res)), 'original_id': mc_id, 'contents': {'context': context, 'questions': questions}})
        
    print 'Extracted (passage,question) pairs:', len(res)
    return res

if __name__=='__main__':
    res = main()
    with open('wdw_data.json', 'w') as fp:
        json.dump(res,fp)

