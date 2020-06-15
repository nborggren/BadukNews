import codecs
def MergeFiles(flist,path='./',write=1,n=-1,name='.merged'):
    f=open('./lists/'+flist)
    files = [line.replace('\n','') for line in f]
    mywords = {}
    mypos = {}
    for j in files:
        g=open(path+j)
        for line in g:
            tmp=line.decode('utf-8').split()
            if len(tmp)>3:
                #print 'error', line
                continue
            try:
                mywords[tmp[0]]+=int(tmp[2])
            except KeyError:
                mywords[tmp[0]]=int(tmp[2])
            mypos[tmp[0]]=tmp[1]

    freq = sorted(mywords.keys(), key=lambda x: mywords[x])
    freq.reverse()
    if write==1:
        dat=codecs.open('./output/'+flist+name,'w',encoding='utf-8')
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

    return mywords,mypos,freq

def WriteList(mywords,mypos,freq,pos='NNG,',name='han.nng'):
    dat=codecs.open('./output/'+name,'w',encoding='utf-8')
    nng = [i for i in freq if mypos[i]==pos]
    print len(nng),pos
    for i in nng:
        try:
            dat.write(i)
            dat.write(' ')
            dat.write(str(mywords[i]))
            dat.write('\n')
        except KeyError:
            continue

mydic,gram,freq = MergeFiles('oro_tot.list')
for i in freq[:50]:
    print i,mydic[i],gram[i]

#mydic,gram,freq = MergeFiles('han_tot.list',write=0)
#for i in freq[:50]:
#    print i,mydic[i],gram[i]

keys = set(gram.values())
print len(keys)
nng = [i for i in freq if gram[i]=='NNG,']
print len(nng)

for i in nng[:20]:print i

for i in keys:
    j=i.replace(',','')
    WriteList(mydic,gram,freq,pos=i,name='oro.'+j)
