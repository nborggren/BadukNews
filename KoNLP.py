import time
import re
import codecs
import urllib2 as ul
import xml.etree.ElementTree as ET
from konlpy.tag import Kkma
from konlpy.utils import pprint

def ReadSent(pageno,src='./han/'):
    dat=codecs.open(src+str(pageno)+'.d',encoding='utf-8')
    dat = dat.read()
    dat = Clean(dat)
    dat = dat.replace('?','.')
    dat = dat.replace('!','.')
    return [' '.join(i.split()) for i in dat.split('.')]
    
def Clean(sentence,comma=0):
    if comma==0:
        for i in ['\n','_','-','(',')','"','\'','...','[',']','<','>','\r']:
            sentence=sentence.replace(i,' ')
    else:
        for i in ['\n','_','-','(',')','"','\'','...','[',']','<','>',',','\r']:
            sentence=sentence.replace(i,' ')
    return sentence.strip()

def LoadDB():
    sent1=[]
    f = open('./lists/han.list')
    for line in f:
        tmp=ReadSent(int(line.split('.')[0]))
        for j in tmp:
            sent1.append(j)

    sent2=[]
    f = open('./lists/dat.list')
    for line in f:
        tmp=ReadSent(int(line.split('.')[0]),src='./dat/')
        for j in tmp:
            sent2.append(j)
        
    sent3=[]
    f = open('./lists/oro.list')
    for line in f:
        tmp=ReadSent(int(line.split('.')[0]),src='./oro/')
        for j in tmp:
            sent3.append(j)

    return sent1+sent2+sent3

sent = LoadDB()
print len(sent)
kkma=Kkma()
for i in sent[:10]:
    print i
    #pprint(kkma.nouns(i))
    pprint(kkma.pos(i))
