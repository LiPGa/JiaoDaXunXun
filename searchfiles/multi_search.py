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
from org.apache.lucene.queryparser.classic import QueryParserBase
from org.apache.lucene.queryparser.classic import MultiFieldQueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.search import BooleanClause
from org.apache.lucene.util import Version
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

def run(searcher, analyzer):
	def scents_search(former,mid,last):
		query=''.join(former)+' '+''.join(mid)+' '+''.join(last)
		fields = ["former_scents", "mid_scents","last_scents"]
		clauses = [ BooleanClause.Occur.SHOULD, BooleanClause.Occur.SHOULD,BooleanClause.Occur.SHOULD]
		parser = MultiFieldQueryParser(Version.LUCENE_CURRENT, fields, analyzer)
		parser.setDefaultOperator(QueryParserBase.AND_OPERATOR)
		query = MultiFieldQueryParser.parse(parser, query)
		return query

	def brand_scent_search(brand,scent):
		query=brand+' '+''.join(scents)
		fields = ["name", "scents"]
		clauses = [ BooleanClause.Occur.SHOULD, BooleanClause.Occur.SHOULD,BooleanClause.Occur.SHOULD]
		parser = MultiFieldQueryParser(Version.LUCENE_CURRENT, fields, analyzer)
		parser.setDefaultOperator(QueryParserBase.AND_OPERATOR)
		query = MultiFieldQueryParser.parse(parser, query)		
		return query

	brand='爱马仕'
	scents=['水仙花','香根草']
	former=['醋栗叶','黑加仑花']
	mid=['水仙花']
	last=['香根草']

	query=brand_scent_search(brand,scents)
	# query=scents_search(former,mid,last)

	scoreDocs = searcher.search(query, 8).scoreDocs

	for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print 'name:',doc.get('name')
            if doc.get('former_scents')!=None:
                print 'former:',doc.get('former_scents')
                print 'mid:',doc.get('mid_scents')
                print 'last:',doc.get('last_scents')
            else:
                print 'scents:',doc.get('scents')
            print '-'*100	

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
