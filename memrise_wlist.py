#encoding: utf-8
from HanLib import *

sent = LoadDB()


m01 = ['것','하다','있다','수','나','없다','않다','사람','우리','그','아니다','보다','저것','보다','같다']
m21 = ['줄','하늘','년대','과학','자연','정말','구조','격국','밥','입다','오히려','프로그램','네','이루어지다','남']

#token = unicode(token,'utf-8')
#test = SearchDB(sent,token)
#print len(test)

WriteList(sent,m01,'mem01')
WriteList(sent,m21,'mem21')
