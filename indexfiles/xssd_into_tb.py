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
    def perfume_search(command,tb_data_line,f):
        query = QueryParser(Version.LUCENE_CURRENT, "name",
                            analyzer).parse(QueryParser.escape(command))
        scoreDocs = searcher.search(query, 1).scoreDocs
        # print "%s total matching documents." % len(scoreDocs)
        contents=tb_data_line.split('\t')
        name=contents[0]
        url=contents[1]
        price=str(contents[2])
        post=str(contents[3])
        sales=str(contents[4][:-3])
        comments=str(contents[5])
        place=contents[6]
        shop=contents[7]
        img=contents[-1]

        for scoreDoc in scoreDocs:
		doc = searcher.doc(scoreDocs[0].doc)
        	data={}
        	data.setdefault('name',name)
        	data.setdefault('url',url)
        	data.setdefault('price',price)
        	data.setdefault('post',post)
        	data.setdefault('sales',sales)
        	data.setdefault('comments',comments)
        	data.setdefault('place',place)
        	data.setdefault('shop',shop)
        	data.setdefault('img',img)

        	data.setdefault('xssd_name',doc.get('name'))
        	data.setdefault('perfumer',doc.get('perfumer'))
		data.setdefault('tune',doc.get('tune'))
		data.setdefault('xssd_url', doc.get('url'))
		data.setdefault('brand',doc.get('brand'))
		data.setdefault('rate:',float(doc.get('rate')))
		data.setdefault('xssd_comments',doc.get('comment'))
		if doc.get('former_scents')!=None:
			former=doc.get('former_scents')
			mid=doc.get('mid_scents')
			last=doc.get('last_scents')
			data.setdefault( 'former',former)
			data.setdefault( 'mid',mid)
			data.setdefault('last',last)
			scents=former+' '+mid+' '+last
			data.setdefault('scents',scents)
		else:
		    data.setdefault( 'scents',doc.get('scents'))

			
		for k,v in data.items():
			if v==None:
				f.write('None'+'\t')
			else:
				f.write(str(v)+'\t')
		f.write('\n')
		# indexer = engine.Indexer()
	      # for i in data.keys():
	      		# indexer.set(i,stored=True, tokenized=True)


    file=open('tabao.txt','r')
    goods_file=open('tb_goods.txt','r')

    tb_lines=file.readlines()
    goods_lines=goods_file.readlines()
    cnt=0
    f=open('whole.txt','w')
    for line in goods_lines:
    	# try:
	index=goods_lines.index(line)
	tb_data_line = tb_lines[index].strip('\n')
	tb_data_line=tb_data_line.decode('utf-8','ignore')
  	good = line.strip('\n')
	perfume_search(good,tb_data_line,f)
	# except Exception,e:
		# print e
    f.close()

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
