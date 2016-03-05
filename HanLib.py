import time
import re
import codecs
import urllib2 as ul
import xml.etree.ElementTree as ET

def ReadSent(pageno,src='./han/'):
    dat=codecs.open(src+str(pageno)+'.d',encoding='utf-8')
    dat = dat.read()
    dat = Clean(dat)
    dat = dat.replace('?','.')
    dat = dat.replace('!','.')
    return [' '.join(i.split()) for i in dat.split('.')]
    
def Clean(sentence,comma=0):
    if comma==0:
        for i in ['\n','_','-','(',')','"','\'',u'▲','...','[',']',u'■','<','>','\r',u'▶',u'◀']:
            sentence=sentence.replace(i,' ')
    else:
        for i in ['\n','_','-','(',')','"','\'',u'▲','...','[',']',u'■','<','>',',','\r']:
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

def ShortSent(sent):
    return sorted(sent, key = lambda x: len(x))

def SearchDB(sent,token):
    matches = [i for i in sent if i.find(token)>0]
    return sorted(matches, key=lambda x: len(x))

def SearchDBList(sent,tokens):
    matches=[]
    for token in tokens:
        matches += [i for i in sent if i.find(token)>0]
    return sorted(matches, key=lambda x: len(x))