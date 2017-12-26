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
        query = QueryParser(Version.LUCENE_CURRENT, "name",
                            analyzer).parse(command)
        scoreDocs = searcher.search(query, 8).scoreDocs
        print "%s total matching documents." % len(scoreDocs)

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print "--------------------------------------------------------"
            print 'perfume:',doc.get('name')
            if doc.get('name')==command:
              print '100% MATCH!'
            print 'perfumer',doc.get('perfumer')
            if doc.get('former_scents')!=None:
                print 'former:',doc.get('former_scents')
                print 'mid:',doc.get('mid_scents')
                print 'last:',doc.get('last_scents')
            else:
                print 'scents',doc.get('scents')
            print 'tune:',doc.get('tune')
            print 'url:', doc.get('url')
            print 'brand:',doc.get('brand')
            print 'rate:',float(doc.get('rate'))
            print 'comments:',doc.get('comment')

    def perfumer_search(command):
        query = QueryParser(Version.LUCENE_CURRENT, "perfumer",
                            analyzer).parse(command)
        scoreDocs = searcher.search(query, 8).scoreDocs
        print "%s total matching documents." % len(scoreDocs)

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print "--------------------------------------------------------"
            print 'perfume:',doc.get('name')
            if doc.get('name')==command:
              print '100% MATCH!'
            print 'perfumer',doc.get('perfumer')
            if doc.get('former_scents')!=None:
                print 'former:',doc.get('former_scents')
                print 'mid:',doc.get('mid_scents')
                print 'last:',doc.get('last_scents')
            else:
                print 'scents:',doc.get('scents')
            print 'tune:',doc.get('tune')
            print 'url:', doc.get('url')
            print 'brand:',doc.get('brand')
            print 'rate:',float(doc.get('rate'))
            print 'comments:',doc.get('comment')

    def scent_search(command):
        query = QueryParser(Version.LUCENE_CURRENT, "former_scents",
                            analyzer).parse(command)
        scoreDocs = searcher.search(query, 8).scoreDocs
        print "%s total matching documents." % len(scoreDocs)

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print "--------------------------------------------------------"
            print 'perfume:',doc.get('name')
            print 'perfumer:',doc.get('perfumer')
            if doc.get('former_scents')!=None:
                print 'former:',doc.get('former_scents')
                print 'mid:',doc.get('mid_scents')
                print 'last:',doc.get('last_scents')
            else:
                print 'scents:',doc.get('scents')
            print 'tune:',doc.get('tune')
            print 'url:', doc.get('url')
            print 'brand:',doc.get('brand')
            print 'rate:',float(doc.get('rate'))
            print 'comments:',doc.get('comment')

    command="法国Hermes爱马仕蓝色橘彩星光女士淡香水EDT50100ml清新礼物包邮"
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
