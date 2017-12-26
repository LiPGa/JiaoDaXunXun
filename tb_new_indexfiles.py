# -*- coding: utf-8 -*-
#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, threading, time, re
from datetime import datetime

from java.io import File
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version

"""
This class is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(root, writer)
        ticker = Ticker()
        print 'commit index',
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print 'done'
    def getTxtAttribute(self, contents, attr):
        m = re.search(attr + ': (.*?)\n',contents)
        if m:
            return m.group(1)
        else:
            return ''


    def indexDocs(self, root, writer):
        t1 = FieldType()
        t1.setIndexed(True)
        t1.setStored(True)
        t1.setTokenized(False)
        t1.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)        

        t2 = FieldType()
        t2.setIndexed(False)
        t2.setStored(True)
        t2.setTokenized(False)
        t2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        t3 = FieldType()
        t3.setIndexed(True)
        t3.setStored(True)
        t3.setTokenized(True)
        t3.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)
        
        
        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:
                if not filename.endswith('.txt'):
                    continue
                print "adding", filename
                try:
                    path = os.path.join(root, filename)
                    file = open(path)
                    cnt=0

                    for line in file.readlines():
                        line=line.strip('\n')
                        line=line.decode('utf-8','ignore')
                        contents=line.split('\t')
                        contents=contents[:-1]
                        # print len(contents) #17 or 20
                        shop=contents[0]
                        perfumer=contents[1]
                        perfumer_flag=True
                        if perfumer=='None':
                            perfumer_flag=False
                        xssd_comments=contents[2]
                        name=contents[3]
                        img=contents[4]
                        url=contents[5]
                        if len(contents)==20:
                            mid=contents[6]
                            price=contents[7]
                            sales=contents[8]
                            comments=contents[9]
                            rate=contents[10]
                            place=contents[11]
                            scents=contents[12]
                            former=contents[13]
                            xssd_name=contents[14]
                            post=contents[15]
                            xssd_url=contents[16]
                            brand=contents[17]
                            tune=contents[18]
                            last=contents[19]
                        elif len(contents)==17:
                            price=contents[6]
                            sales=contents[7]
                            comments=contents[8]
                            rate=contents[9]
                            place=contents[10]
                            scents=contents[11]
                            xssd_name=contents[12]
                            post=contents[13]
                            xssd_url=contents[14]
                            brand=contents[15]
                            tune=contents[16]
                        else:
                            print len(contents)
                        tune_flag=True
                        if tune=='None':
                            tune_flag=False
                        try:
                            doc = Document()
                            doc.add(Field("name", name,t3))    
                            doc.add(Field("url", url,t2))        
                            doc.add(Field("price", price,t3))
                            doc.add(Field("post",post,t3))        
                            doc.add(Field("sales",sales,t3))        
                            doc.add(Field("comments",comments,t3))        
                            doc.add(Field("place",place,t2))        
                            doc.add(Field("shop",shop,t2))        
                            doc.add(Field("img",img, t2))
                            if perfumer_flag:
                                doc.add(Field("perfumer",perfumer, t3))
                            if tune_flag:
                                doc.add(Field("tune",tune, t3))
                            doc.add(Field("xssd_comments",xssd_comments, t2))
                            doc.add(Field("scents",scents, t3))
                            doc.add(Field("rate",rate, t2))
                            doc.add(Field("xssd_url",xssd_url, t2))
                            doc.add(Field("brand",brand, t3))
                            doc.add(Field("former",former, t3))
                            doc.add(Field("mid",mid, t3))
                            doc.add(Field("last",last, t3))
                            doc.add(Field("xssd_name",xssd_name, t3))
                        except Exception,e:
                            print "Failed in indexDocs:", e
                            print line
                            print cnt
                        cnt+=1
                        writer.addDocument(doc)
                        # writer.optimize()
                except Exception, e:
                    print "Failed in indexDocs:", e

if __name__ == '__main__':
    """
    if len(sys.argv) < 2:
        print IndexFiles.__doc__
        sys.exit(1)
    """
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    try:
        """
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        IndexFiles(sys.argv[1], os.path.join(base_dir, INDEX_DIR),
                   StandardAnalyzer(Version.LUCENE_CURRENT))
                   """
        analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
        IndexFiles('new_tb', "index_tb_new", analyzer)
        end = datetime.now()
        print end - start
    except Exception, e:
        print "Failed: ", e
        raise e
