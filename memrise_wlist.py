#encoding: utf-8
from HanLib import *

sent = LoadDB()


m21 = ['줄','하늘','년대','과학','자연','정말','구조','격국','밥','입다','오하려','프로그램','네','이루어지다','남']

#token = unicode(token,'utf-8')
#test = SearchDB(sent,token)
#print len(test)

WriteList(sent,m21,'mem21')
