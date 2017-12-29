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
from org.apache.lucene.queryparser.classic import QueryParserBase
from org.apache.lucene.queryparser.classic import MultiFieldQueryParser
from org.apache.lucene.search import BooleanClause
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
        return query

    def cross_search(former,mid,last):
        query=''.join(former)+' '+''.join(mid)+' '+''.join(last)
        fields = ["former", "mid","last"]
        clauses = [ BooleanClause.Occur.SHOULD, BooleanClause.Occur.SHOULD,BooleanClause.Occur.SHOULD]
        parser = MultiFieldQueryParser(Version.LUCENE_CURRENT, fields, analyzer)
        parser.setDefaultOperator(QueryParserBase.AND_OPERATOR)
        query = MultiFieldQueryParser.parse(parser, query)
        return query

    def former_search(former):
        query = QueryParser(Version.LUCENE_CURRENT, "former",analyzer).parse(command)
        return query
    def mid_search(mid):
        query = QueryParser(Version.LUCENE_CURRENT, "mid",analyzer).parse(command)
        return query
    def last_search(last):
        query = QueryParser(Version.LUCENE_CURRENT, "last",analyzer).parse(command)
        return query
    def brand_scent_search(brand,scent):
        query=brand+' '+''.join(scents)
        fields = ["xssd_name", "scents"]
        clauses = [ BooleanClause.Occur.SHOULD, BooleanClause.Occur.SHOULD,BooleanClause.Occur.SHOULD]
        parser = MultiFieldQueryParser(Version.LUCENE_CURRENT, fields, analyzer)
        parser.setDefaultOperator(QueryParserBase.AND_OPERATOR)
        query = MultiFieldQueryParser.parse(parser, query)      
        return query     


    def standard_sort(query):
        scoreDocs=searcher.search(query,8).scoreDocs
        return scoreDocs

    def price_sort(query):
        scoreDocs = searcher.search(query, 8 , Sort([SortField.FIELD_SCORE,SortField("price", SortField.Type.DOUBLE,False),
                                     SortField("sales", SortField.Type.INT,True)])).scoreDocs
        return scoreDocs

    def sales_sort(query):
        scoreDocs = searcher.search(query, 8 , Sort([SortField.FIELD_SCORE,SortField("sales", SortField.Type.INT,True),
                                     SortField("price", SortField.Type.DOUBLE,False)])).scoreDocs
        return scoreDocs

    brand='爱马仕'
    # brand='Hermes'
    scents=['水仙花','香根草']
    command="绿邂逅"
    former=['醋栗叶','黑加仑花']
    mid=['水仙花']
    last=['香根草']

    # query=cross_search(former,mid,last)
    query=brand_scent_search(brand,scents)
    # query=perfume_search(command)
    scoreDocs=sales_sort(query)
    # scoreDocs=price_sort(query)
    # scoreDocs=standard_sort(query)
    print "%s total matching documents." % len(scoreDocs)
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        print '-'*100   
        print 'name:',doc.get('name')
        print 'price:',doc.get('price')
        if doc.get('tune')!=None:
            print 'tune:',doc.get('tune')
        print 'Sales:',doc.get('sales')
        if doc.get('former')!=None:
            print 'former:',doc.get('former')
            print 'mid:',doc.get('mid')
            print 'last:',doc.get('last')
        else:
            print 'scents:',doc.get('scents')

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
