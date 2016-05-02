# This Python file uses the following encoding: utf-8
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
    matches = list(set(matches))
    return sorted(matches, key=lambda x: len(x))

def SearchDBList(sent,tokens):
    matches=[]
    for token in tokens:
        matches += [i for i in sent if i.find(token)>0]
    return sorted(matches, key=lambda x: len(x))

def Simplify(sent):
    return list(set(sent))

#a la https://github.com/mouuff/Google-Translate-API/blob/master/python/GoogleTranslate.py
def google_translate(to_translate, to_langage="auto", langage="auto"):
    to_translate=to_translate.encode('utf-8')
    agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
    before_trans = 'class="t0">'
    link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s"% (to_langage, langage, to_translate.replace(" ", "+"))
    request = ul.Request(link, headers=agents)
    page = ul.urlopen(request).read()
    result = page[page.find(before_trans)+len(before_trans):]
    result = result.split("<")[0]
    return result

def LoadWordBank(wbank,path='./xml/'):
    tree = ET.parse(path+wbank)
    root = tree.getroot()
    mywords={}
    for j,k in zip(root.iter('Word'),root.iter('English')):
        mywords[j.text]=k.text
    return mywords

def WCount(sent,write=0,n=2000,name='freq.wlist'):
    mywords={}
    for i in sent:
        i=i.replace(',','')
        for j in i.split():
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
                dat.write(', '+translate(i))
                dat.write('\n')
            except UnicodeDecodeError:
                continue
        
    return mywords, freq
        
def LoadFreqList(name,src='./output/'):
    f = open(src+name)
    keys=[]
    vals=[]
    for line in f:
        tmp = line.decode('utf-8').split(',')
        keys.append(tmp[0])
        vals.append(int(tmp[1]))
    return keys,vals

def MergeFreqList(name1,name2):
    dic1={}
    keys,vals=LoadFreqList(name1)
    keys1,vals1=LoadFreqList(name2)
    for i,j in zip(keys,vals):
        dic1[i]=j
    for i,j in zip(keys1,vals1):
        try:
            dic1[i]+=j
        except KeyError:
            dic1[i]=j
    keyt=sorted(dic1.keys(), key=lambda x: dic1[x])
    keyt.reverse()
    valt=[dic1[i] for i in keyt]
    return keyt,valt
    
def WithRoot(sent, word):
    tmp = set()
    for i in sent:
        t1=i.split()
        for j in t1:
            if j.find(word)>-1:
                tmp.add(j)
    return list(tmp)

def WriteSent(sent,name,translate=1,n=25):
    dat=codecs.open('./output/'+name+'.txt','w',encoding='utf-8')
    for i in sent[:min([len(sent),n])]:
        if translate==1:
            dat.write(i)
            dat.write(', '+google_translate(i))
            dat.write('\n')
        else:
            dat.write(i+'\n')

def WriteList(sent,mylist,name,translate=1,n=25,space=1):
    dat=codecs.open('./output/'+name+'.txt','w',encoding='utf-8')
    if space==1:
        mylist=[' '+word+' ' for word in mylist]
    for word in mylist:
        word = unicode(word,'utf-8')
        tmp = SearchDB(sent,word)
        tmpn = min([n,len(tmp)])
        try:
            dat.write(word+', '+google_translate(word)+'\n')
        except UnicodeDecodeError:
            print word
            dat.write(word+'\n')
        for i in tmp[:tmpn]:
            #i=unicode(i,'utf-8')
            if translate==1:
                try:
                    dat.write(i)
                    dat.write(', '+google_translate(i))
                    dat.write('\n')
                except UnicodeDecodeError:
                    dat.write(i+'\n')
            else:
                dat.write(i+'\n')
        dat.write('\n')
            
