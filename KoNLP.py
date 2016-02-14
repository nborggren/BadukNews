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

def WCount(sent,kkma,write=0,n=2000,name='konlp.wlist'):
    mywords={}
    for i in sent:
        morphs=kkma.morphs(i)
        for j in morphs:
            try:
                mywords[j]+=1
            except KeyError:
                mywords[j]=1
    freq = sorted(mywords.keys(), key=lambda x: mywords[x])
    freq.reverse()
    if write==1:
        dat=codecs.open('./output/'+name,'w',encoding='utf-8')
        for i in freq[:n]:
            try:
                dat.write(i)
                #dat.write(', '+translate(i))
                dat.write('\n')
            except UnicodeDecodeError:
                continue
    return mywords,freq

def WCountPos(sent,kkma,write=0,n=2000,name='konlp.wlist'):
    mywords={}
    mypos={}
    for i in sent:
        pos=kkma.pos(i)
        for j in pos:
            #print j,j[0],j[1]
            #zwom=input("sheat")
            try:
                mywords[j[0]]+=1
            except KeyError:
                mywords[j[0]]=1
            mypos[j[0]]=j[1]
            
    freq = sorted(mywords.keys(), key=lambda x: mywords[x])
    freq.reverse()
    if write==1:
        dat=codecs.open('./output/'+name,'w',encoding='utf-8')
        for i in freq[:n]:
            try:
                dat.write(i)
                dat.write(', ')
                dat.write(mypos[i])
                dat.write(', ')
                dat.write(str(mywords[i]))
                dat.write('\n')
            except KeyError:
                continue
    return mywords, freq



sent = LoadDB()
print len(sent)
kkma=Kkma()
# morphs = []
# pos = []

# for i in sent[:10]:
#     #print i
#     #pprint(kkma.nouns(i))
#     #pprint(kkma.pos(i))
#     morphs+=kkma.morphs(i)
#     pos+=kkma.pos(i)

# print len(morphs),len(set(morphs))
# print len(pos),len(set(pos))

# for i in pos:
#     print i[0],i[1]

a=time.time()
morphs,freq=WCountPos(sent[:100000],kkma,write=1,n=-1,name='pos.list')
b=time.time()
print (b-a)/60.,' minutes passed'
for i in freq[:10]:
    print i

