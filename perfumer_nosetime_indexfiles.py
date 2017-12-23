# -*- coding: utf-8 -*-

#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, threading, time, re
from datetime import datetime

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.search import IndexSearcher
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
        def perfume_search(command):
            query = QueryParser(Version.LUCENE_CURRENT, "perfume",
                                analyzer).parse(command)
            scoreDocs = searcher.search(query, 1).scoreDocs
            print "%s total matching documents." % len(scoreDocs)

            for scoreDoc in scoreDocs:
                doc = searcher.doc(scoreDoc.doc)
                print "--------------------------------------------------------"
                print 'perfume:',doc.get('perfume')
                if doc.get('perfume')==command:
                  print 'MATCH!'
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
        def nosetime_index(file):
            try:
                    f=open('nosetime-perfumer.txt','r')
                    targets=[]
                    for i in f.readlines():
                        i=i.strip('\n')
                        targets.append(i)
                    perfume_list=[]
                    brand_list=[]
                    cnt=0

                    for line in file.readlines():
                        line=line.strip('\n')
                        line=line.decode('utf-8','ignore')
                        contents=line.split('\t')
                        name=contents[1]
                        if name in targets:
                            # print name
                            url=contents[0]
                            brand=name.split(' ')[0]
                            scents=contents[2].strip()
                            scents_list=get_scents(scents)

                            comments=contents[-1][:-2]
                            rate=contents[-2][:-1]

                            try:
                                # contents = file.read().decode('utf8', 'ignore')
                                # file.close()
                                doc = Document()
                                doc.add(Field("url", url,t1))        
                                doc.add(Field("brand", brand,t1))        

                                # doc.add(Field("name", perfume,t3))

                                doc.add(Field("name",name, t3))

                                if name not in perfume_list:
                                    perfume_list.append(name)
                                    print 'add sucessfully perfume:',name
                                if brand not in brand_list:
                                    brand_list.append(brand)

                                doc.add(Field("comment",comments, t2))
                                doc.add(Field("rate",rate, t2))

                                if type(scents_list[0])!=list:
                                    scents=' '.join(scents_list)
                                    doc.add(Field("scents",scents, t3))
                                else:
                                    former_scents=' '.join(scents_list[0])
                                    doc.add(Field("former_scents",former_scents,t3))
                                    mid_scents=' '.join(scents_list[1])
                                    doc.add(Field("mid_scents",mid_scents,t3))
                                    last_scents=' '.join(scents_list[2])
                                    doc.add(Field("last_scents",last_scents,t3))
                            except Exception,e:
                                print "Failed in indexDocs:", e
                                print line
                                print cnt
                            cnt+=1
                            writer.addDocument(doc)
                            # writer.optimize()
            except Exception, e:
                    print "Failed in indexDocs:", e

            # for brand in brand_list:
            #         print brand
                           
        def perfumer_index(file):
            try:
                    perfumer_list=[]
                    cnt=0
                    for line in file.readlines():
                        line=line.strip('\n')
                        line=line.decode('utf-8','ignore')
                        contents=line.split('\t')
                        perfumer=contents[-1]
                        url=contents[0]
                        name=contents[1]
                        scents=contents[2]
                        comments=contents[-2][:-2]
                        rate=contents[-3][:-1]
                        scents_list=get_scents(scents)

                        try:
                            # contents = file.read().decode('utf8', 'ignore')
                            # file.close()
                            doc = Document()
                            doc.add(Field("url", url,t1))                    
                            doc.add(Field("name", name,t3))

                            doc.add(Field("perfumer",perfumer, t3))

                            if perfumer not in perfumer_list:
                                perfumer_list.append(perfumer)
                                print 'add sucessfully',perfumer

                            doc.add(Field("comment",comments, t1))
                            doc.add(Field("rate",rate, t1))
                            if type(scents_list[0])!=list:
                                scents=' '.join(scents_list)
                                doc.add(Field("scents",scents, t3))
                            else:
                                former_scents=' '.join(scents_list[0])
                                doc.add(Field("former_scents",former_scents,t3))
                                mid_scents=' '.join(scents_list[1])
                                doc.add(Field("mid_scents",mid_scents,t3))
                                last_scents=' '.join(scents_list[2])
                                doc.add(Field("last_scents",last_scents,t3))
                        except Exception,e:
                            print "Failed in indexDocs:", e
                            print line
                            print cnt
                        cnt+=1
                        writer.addDocument(doc)
            except Exception, e:
                print "Failed in indexDocs:", e

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
                path = os.path.join(root, filename)
                file = open(path)
                if filename=='aperfumer.txt':
                    perfumer_index(file)
                if filename=='nosetime.txt':
                    nosetime_index(file)
                


if __name__ == '__main__':
    """
    if len(sys.argv) < 2:
        print IndexFiles.__doc__
        sys.exit(1)
    """
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    # base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
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
