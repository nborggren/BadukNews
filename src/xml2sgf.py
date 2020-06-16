
from zipfile import ZipFile
import io
from bs4 import BeautifulSoup as bs

z = ZipFile('../scraped/hangames/gogames_xml.zip')

def readfilefromzip(z, i):
    h = z.open(i, 'r')
    game_string = io.TextIOWrapper(h).read()
    return game_string

bfile = []
with ZipFile('../scraped/sgfs/sgfs.zip', 'w') as s:
    for q in z.filelist:
        try:
            gibo = bs(readfilefromzip(z, q), "lxml")
            name = q.filename.replace('.xml', '.sgf')
            try:
                s.writestr(name, gibo.gibodata.text)
            except AttributeError:
                bfile.append(q)
        except UnicodeDecodeError:
            bfile.append(q)
            continue
s.close()

print(len(bfile))