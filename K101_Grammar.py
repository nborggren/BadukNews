#encoding: utf-8
from HanLib import *

sent = LoadDB()

#K101 - BS4 -17


#K101 - BS4 - 17
pook = SearchDB(sent,u' 푹 ')
WriteSent(pook,'K101_BS4_17_pook',n=100)

#K101 - BS4 - 18
haru = SearchDB(sent,u' 하루에 ')
WriteSent(haru,'K101_BS4_18_haru',n=100)
