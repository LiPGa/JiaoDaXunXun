# -*- coding: utf-8 -*-
#!/usr/bin/env python
INDEX_DIR = "IndexFiles.index"

import sys
import os
import lucene
from java.io import File
from org.apache.lucene import search
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.pylucene.search import PythonFieldComparator, PythonFieldComparatorSource
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import Sort
from org.apache.lucene.search import SortField
from lupyne import engine

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
        scoreDocs = searcher.search(query, 20).scoreDocs
        print "%s total matching documents." % len(scoreDocs)

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print "-"*100
                            #             doc.add(Field("name", name,t3))        
                            # doc.add(Field("url", url,t2))        
                            # doc.add(Field("price", price,t2))
                            # doc.add(Field("post",post,t2))        
                            # doc.add(Field("sales",sales,t2))        
                            # doc.add(Field("comments",comments,t2))        
                            # doc.add(Field("place",place,t2))        
                            # doc.add(Field("shop",shop,t2))        
                            # doc.add(Field("img",img, t2))
            print 'perfume:',doc.get('name')
            if doc.get('name')==command:
              print '100% MATCH!'
            print 'xssd name:',doc.get('xssd_name')
            if doc.get('former')!=None:
                print 'former:',doc.get('former')
                print 'mid:',doc.get('mid')
                print 'last:',doc.get('last')
            else:
                print 'scents:',doc.get('scents')
            print 'tune:',doc.get('tune')
            print 'brand:',doc.get('brand')

    def price_sort(command):
        query = QueryParser(Version.LUCENE_CURRENT, "name",
                            analyzer).parse(command)
        scoreDocs = searcher.search(query, 8).scoreDocs
        print "%s total matching documents." % len(scoreDocs)
        indexer = engine.Indexer()
        l='name','price','comments','sales','url','img','place','shop'
        for i in l:
            indexer.set(i,stored=True, tokenized=False)
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)          
            indexer.add(name=doc.get('name'),price=doc.get('price'),comments=doc.get('comments'),sales=doc.get('sales'),url=doc.get('url'),img=doc.get('img'),shop=doc.get('shop'),place=doc.get('place'))
            # print doc.get('name')
        indexer.commit()
        hits = indexer.search(sort='price')
        for hit in hits:
            print '------------------------------------------------------------------------------------------------------------'
            print 'Perfume:',hit['name']
            print 'Price:',hit['price']
            print 'img:',hit['img']
            print 'Sales:',hit['sales']
            print 'comments:',hit['comments']
            print 'Shop:',hit['shop']
            print 'Place:',hit['place']
    def sales_sort(command):
        query = QueryParser(Version.LUCENE_CURRENT, "name",
                            analyzer).parse(command)
        scoreDocs = searcher.search(query, 8).scoreDocs
        # sorter = search.Sort(search.SortField('price', search.SortField.Type.STRING))
        # topdocs = searcher.search(query, None, 10, sorter)
        # print "%s total matching documents." % len(topdocs.scoreDocs)
        # for scoredoc in topdocs.scoreDocs:
        #     doc = searcher.doc(scoredoc.doc)
        print "%s total matching documents." % len(scoreDocs)
        indexer = engine.Indexer()
        l='name','price','comments','sales','url','img','place','shop'
        for i in l:
            indexer.set(i,stored=True, tokenized=False)
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)          
            indexer.add(name=doc.get('name'),price=doc.get('price'),comments=doc.get('comments'),sales=doc.get('sales'),url=doc.get('url'),img=doc.get('img'),shop=doc.get('shop'),place=doc.get('place'))
            # print doc.get('sales')
        indexer.commit()
        hits = list(indexer.search(sort='sales'))[::-1]
        for hit in hits:
            print '------------------------------------------------------------------------------------------------------------'
            print 'Perfume:',hit['name']
            print 'Price:',hit['price']
            print 'Sales:',hit['sales']
            print 'img:',hit['img']
            print 'comments:',hit['comments']
            print 'Shop:',hit['shop']
            print 'Place:',hit['place']

    command="爱马仕大地"
    perfume_search(command)


if __name__ == '__main__':
    STORE_DIR = "index_tb_new"
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    # base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))    
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    run(searcher, analyzer)
    del searcher
