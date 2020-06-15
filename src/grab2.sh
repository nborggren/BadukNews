#!/bin/bash
curl 'http://baduk.hangame.com/giboxml.nhn?gseq='$1 -H 'Host: baduk.hangame.com' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:44.0) Gecko/20100101 Firefox/44.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate' -H 'Referer: http://baduk.hangame.com/share/flashgibo/viewer.swf' -H 'Cookie: NNB=GHHWT5IEQKFVM; BID=QOIW72UKEOEVE8C1EEIAKY4CY; JSESSIONID=BA4836114C100248B530A064B495DD0D; ACEFCID=UID-56CF53D66AD3590A86B2749C; ACEUCI=1' -H 'Connection: keep-alive' > ./hangames/$1.xml


