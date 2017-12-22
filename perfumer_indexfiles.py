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
    def perfumer_search(command):
        query = QueryParser(Version.LUCENE_CURRENT, "name",
                            analyzer).parse(command)
        scoreDocs = searcher.search(query, 50).scoreDocs
        print "%s total matching documents." % len(scoreDocs)

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print "--------------------------------------------------------"
            print 'perfume:',doc.get('perfume')
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
            if doc.get('scents')==None:
                print 'former:',doc.get('former_scents')
                print 'mid:',doc.get('mid_scents')
                print 'last:',doc.get('last_scents')
            else:
                print 'scents',doc.get('scents')
            print 'url:', doc.get('url')
            print 'rate:',doc.get('rate')
    while True:
        print
        print "Hit enter with no input to quit."
        choice=raw_input('1-perfumer, 2-scents:')
        if choice=='':
            return
        command = raw_input("Query:")
        command = unicode(command, 'utf-8')
        if choice=='1':
            perfumer_search(command)
        if choice=='2':
            scent_search(command)
        if command == '':
            return
        print "Searching for:", command


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
