# -*- coding: utf-8 -*-
#!/usr/bin/env python
INDEX_DIR = "IndexFiles.index"

import sys
import os
import lucene
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
"""
This script is loosely based on the Lucene (java implementation) demo class
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""


def run(searcher, analyzer):
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
            print 'perfumer',doc.get('name')
            if doc.get('scents')==None:
                print 'former:',doc.get('former_scents')
                print 'mid:',doc.get('mid_scents')
                print 'last:',doc.get('last_scents')
            else:
                print 'scents',doc.get('scents')
            print 'url:', doc.get('url')
            print 'rate:',doc.get('rate')
    def perfumer_search(command):
        query = QueryParser(Version.LUCENE_CURRENT, "name",
                            analyzer).parse(command)
        scoreDocs = searcher.search(query, 50).scoreDocs
        print "%s total matching documents." % len(scoreDocs)

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print "--------------------------------------------------------"
            print 'perfume:',doc.get('perfume')
            print 'perfumer',doc.get('name')
            if doc.get('scents')==None:
                print 'former:',doc.get('former_scents')
                print 'mid:',doc.get('mid_scents')
                print 'last:',doc.get('last_scents')
            else:
                print 'scents',doc.get('scents')
            print 'url:', doc.get('url')
            print 'rate:',doc.get('rate')

    def scent_search(command):
        query = QueryParser(Version.LUCENE_CURRENT, "scents",
                            analyzer).parse(command)
        scoreDocs = searcher.search(query, 50).scoreDocs
        print "%s total matching documents." % len(scoreDocs)

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print "--------------------------------------------------------"
            print 'perfume:',doc.get('perfume')
            print 'perfumer',doc.get('name')
            if doc.get('scents')==None:
                print 'former:',doc.get('former_scents')
                print 'mid:',doc.get('mid_scents')
                print 'last:',doc.get('last_scents')
            else:
                print 'scents',doc.get('scents')
            print 'url:', doc.get('url')
            print 'rate:',doc.get('rate')

    command="现货 法国爱马仕蓝色海洋橘彩星光香水2017年新品蔚蓝100ml"
    perfume_search(command)


if __name__ == '__main__':
    STORE_DIR = "index"
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    # base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    run(searcher, analyzer)
    del searcher
