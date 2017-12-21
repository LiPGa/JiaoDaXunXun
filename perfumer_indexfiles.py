# -*- coding: utf-8 -*-

#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, threading, time, re
from datetime import datetime

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
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
        def get_scents(scents):
        # [[前调们],[中调],[后调]]
            scents_list=[]
            if scents[:3]=='气味：':
                scents=scents[3:]
                scents_list=scents.split(',')
            else:
                if scents[:3]=='前调：':
                    mid_scent_index=scents.find('中调：')
                    last_scent_index=scents.find('后调：')
                    
                    former_scents=scents[3:mid_scent_index]
                    former_scents_list=former_scents.split(',')
                    scents_list.append(former_scents_list)

                    mid_scents= scents[mid_scent_index+3:last_scent_index]
                    mid_scents_list=mid_scents.split(',')
                    scents_list.append(mid_scents_list)
                    
                    last_scents= scents[last_scent_index+3:]
                    last_scents_list=last_scents.split(',')
                    scents_list.append(last_scents_list)
            return scents_list

        t1 = FieldType()
        t1.setIndexed(True)
        t1.setStored(True)
        t1.setTokenized(False)
        t1.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)        

        t3 = FieldType()
        t3.setIndexed(True)
        t3.setStored(True)
        t3.setTokenized(True)
        t3.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)
        
        t2 = FieldType()
        t2.setIndexed(True)
        t2.setStored(False)
        t2.setTokenized(False)
        t2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
        
        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:
                if not filename.endswith('.txt'):
                    continue
                print "adding", filename
                try:
                    path = os.path.join(root, filename)
                    file = open(path)
                    perfumer_list=[]
                    cnt=0
                    for line in file.readlines():
                        line=line.strip('\n')
                        line=line.decode('utf-8','ignore')
                        contents=line.split('\t')
                        name=contents[-1]
                        url=contents[0]
                        perfume=contents[1]
                        scents=contents[2]
                        comments=contents[-2][:-2]
                        rate=contents[-3][:-1]
                        scents_list=get_scents(scents)

                        try:
                            # contents = file.read().decode('utf8', 'ignore')
                            # file.close()
                            doc = Document()
                            doc.add(Field("url", url,t1))                    
                            doc.add(Field("perfume", perfume,t3))

                            doc.add(Field("name",name, t3))

                            if name not in perfumer_list:
                                perfumer_list.append(name)
                                print 'add sucessful',name

                            doc.add(Field("comment",comments, t2))
                            doc.add(Field("rate",rate, t2))
                            if type(scents_list[0])!=list:
                                for scent in scents_list:
                                    doc.add(Field("scents",scent, t1))
                            else:
                                for former_scent in scents_list[0]:
                                    doc.add(Field("former_scents",former_scent,t1))
                                for mid_scent in scents_list[1]:
                                    doc.add(Field("mid_scents",mid_scent,t1))
                                for last_scent in scents_list[2]:
                                    doc.add(Field("last_scents",mid_scent,t1))
                        except Exception,e:
                            print "Failed in indexDocs:", e
                            print line
                            print cnt
                        cnt+=1
                        writer.addDocument(doc)
                except Exception, e:
                    print "Failed in indexDocs:", e

                    # print line

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
        IndexFiles('testfolder', "index", analyzer)
        end = datetime.now()
        print end - start
    except Exception, e:
        print "Failed: ", e
        raise e
