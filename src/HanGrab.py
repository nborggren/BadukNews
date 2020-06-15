import requests 
from bs4 import BeautifulSoup as bs
import time
import re
import codecs
from glob import glob
import time

def HanParse(pageno,write=0):
    newspage = requests.get('http://baduk.hangame.com/news.nhn?gseq='+str(pageno)+'&m=view&page=1&searchfield=&leagueseq=0&searchtext=')
    soup = bs(newspage.content,'html.parser')
    #[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
    tmp = soup.getText()
    tmp=u'내용'.join(tmp.split(u'내용')[2:])
    b=tmp.find(u'관련 뉴스보기')
    tmp=tmp[:b]
    tmp='\n'.join([i for i in tmp.split('\n') if len(i)>0])
    if write==1:
        h=codecs.open('./han/'+str(pageno)+'.d','w',encoding='utf-8')
        h.write(tmp)
    return tmp

def TyParse(pageurl, write=0):
    url = "http://news.tygem.com/news/tnews/{}".format(pageurl)
    newspage = requests.get(url)
    soup = bs(newspage.content,'html.parser')
    #[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
    tmp = soup.getText()
    #print(tmp)
    #zwom = input("sheat")
    a=tmp.find(u'바둑뉴스')
    b=tmp.find(u'TYGEM / ')
    tmp = [i for i in tmp[a:b].split('\n') if len(i)>0]
    vtext = '\n'.join(tmp[1:])
    if write==1:
        pageno = pageurl.split('seq=')[-1].split('&')[0]
        h=codecs.open('./tygem/'+str(pageno)+'.d','w',encoding='utf-8')
        h.write(vtext)
    return vtext

def OroParse(pageno,write=0):
    newspage = requests.get('http://www.cyberoro.com/news/news_view.oro?div_no=A1&num='+str(pageno)+'&pageNo=1&cmt_n=0')
    soup = bs(newspage.content,'html.parser')
    #[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
    tmp = soup.getText()
    a=tmp.find(u'Home > 뉴스')
    b=tmp.find(u'┃관련뉴스')
    tmp = tmp[a:b]
    tmp = [i for i in tmp.split('\n')[1:] if len(i)>0]
    vis = '\n'.join(tmp)
    if write==1:
        h=codecs.open('./oro/'+str(pageno)+'.d','w',encoding='utf-8')
        h.write(vis)
    return vis

def GetSent(pageno):
    dat=HanParse(pageno)
    sent = dat.split('.')[6:-1]
    first = sent[0].split(u'내용')
    sent[0]=first[-1]
    return sent[:-3]

def ReadSent(pageno,src='./han/'):
    dat=codecs.open(src+str(pageno)+'.d',encoding='utf-8')
    dat = dat.read()
    dat = Clean(dat)
    dat = dat.replace('?','.')
    dat = dat.replace('!','.')
    return [' '.join(i.split()) for i in dat.split('.')]
    
def Clean(sentence,comma=0):
    if comma==0:
        for i in ['\n','_','-','(',')','"','\'',u'▲','...','[',']',u'■','<','>','\r']:
            sentence=sentence.replace(i,' ')
    else:
        for i in ['\n','_','-','(',')','"','\'',u'▲','...','[',']',u'■','<','>',',','\r']:
            sentence=sentence.replace(i,' ')
    return sentence.strip()

def GetArticles(indexno, src='han'):

    articles = []

    pass


def GetHanArticles(indexno):
    articles=[]
    main=requests.get('http://baduk.hangame.com/news.nhn?&page='+str(indexno))
    mainbs=bs(main.content,'html.parser')
    tmp = [link.get('href') for link in mainbs.find_all('a')]
    for j in tmp:
        try:
            if j.find('readnews')>0:
                articles.append(j)
        except AttributeError:
            continue
    mynews=[int(re.search(r'\d+', i).group()) for i in articles]
    mynews = sorted(list(set(mynews)))
    return mynews

def GetTyArticles(indexno):
    articles=[]
    main=requests.get('http://news.tygem.com/news/tnews/main.asp?pagec='+str(indexno))
    mainbs=bs(main.content,'html.parser')
    
    tmp = [link.get('href') for link in mainbs.find_all('a')]
    for j in tmp:
        try:
            if j.find('view.asp?')>-1:
                articles.append(j)
        except AttributeError:
            continue
    return articles

def GetOroArticles(pageno):
    articles=[]
    loc="http://cyberoro.com/news/news_list.oro?cmt_n=0&div_no=A1&pageNo="+str(pageno)+"&blockNo=1"
    newspage = requests.get(loc)
    soup = bs(newspage.content,'html.parser')
    tmp = [link.get('href') for link in soup.find_all('a')]
    for j in tmp:
        try:
            if j.find('news_view.oro?pageNo=')>0:
                articles.append(j)
        except AttributeError:
            continue
    articles = [i[i.find('num'):] for i in articles]
    mynews=[int(re.search(r'\d+', i).group()) for i in articles]
    return mynews

def WordCount(pagelist,sort=1,sentence=0):
    sentences=[]
    words=[]
    for page in pagelist:
        
        tmp=GetSent(page)
        for sent in tmp:
            sentences.append(Clean(sent))
    for sent in sentences:
        for j in sent.split():
            words.append(j)
    uwords = list(set(words))
    wc = [(i,words.count(i)) for i in uwords]
    if sort==1:
        wc = sorted(wc, key=lambda x: x[1])
        wc.reverse()
    if sentence==0:
        return wc
    else:
        return wc, sentence

#a la https://github.com/mouuff/Google-Translate-API/blob/master/python/GoogleTranslate.py
def translate(to_translate, to_langage="auto", langage="auto"):
    to_translate=to_translate.encode('utf-8')
    agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
    before_trans = 'class="t0">'
    link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s"% (to_langage, langage, to_translate.replace(" ", "+"))
    request = requests.get(link, headers=agents)
    page = request.content
    result = page[page.find(before_trans)+len(before_trans):]
    result = result.split("<")[0]
    return result

def UpdateData(src='han', start=1, sleep=5):

    if src=='han':
        files = [line.split('/')[-1].split('.')[0] for line in glob('./han/*')]
        cnt=start
        articles=GetHanArticles(start)

        checks = [i in files for i in articles]
        print(checks)
        while checks.count(True)==0 :

            print( 'updating ', len(articles), 'hangame files' )   
            for i in articles:
                print(i)
                time.sleep(sleep)
                HanParse(i,write=1)
            files = [line.split('/')[-1].split('.')[0] for line in glob('./han/*')]
            cnt+=1
            articles=GetHanArticles(cnt)
            checks = [i in files for i in articles]
            print( cnt)
            articles=[j for j in articles if j not in files]

        return articles
    
    if src=='tygem':
        files = [line.split('/')[-1].split('.')[0] for line in glob('./tygem/*')]
        cnt=start
        articles=GetTyArticles(start)

        checks = [i in files for i in articles]
        print(checks)
        while checks.count(True)==0 :

            print( 'updating ', len(set(articles)), 'tygem files' )   
            for i in articles:
                time.sleep(sleep)
                TyParse(i,write=1)
            files = [line.split('/')[-1].split('.')[0] for line in glob('./tygem/*')]
            cnt+=1
            articles=GetTyArticles(cnt)
            checks = [i in files for i in articles]
            print( cnt)
            articles=[j for j in articles if j not in files]

        return list(set(articles))

    if src=='oro':
        files = [line.split('/')[-1].split('.')[0] for line in glob('./oro/*')]
        articles=GetOroArticles(start)
        cnt=start
        checks = [i in files for i in articles]
        while checks.count(True)==0 :
            cnt+=1
            articles=GetOroArticles(cnt)
            checks = [i in files for i in articles]
            print( cnt)
            articles=[j for j in articles if j not in files]
            print( 'updating ', len(articles), ' oro files' )   
            for i in articles:OroParse(i,write=1)
            files = [line.split('/')[-1].split('.')[0] for line in glob('./oro/*')]
        return 
    
    if src=='all':
        articles=UpdateData(src='han')
        articles+=UpdateData(src='ty')
        articles+=UpdateData(src='oro')
        return articles

def MergeWords():
    pass