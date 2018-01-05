# -*- coding: utf-8 -*-
import web
render = web.template.render('templates/')

from web import form
import urllib2

INDEX_DIR = "IndexFiles.index"

import re
import sys
import os
import lucene
import threading
import urllib2

import json
reload(sys)
sys.setdefaultencoding('utf-8')
from java.io import File
from org.apache.lucene import search
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.search.highlight import Highlighter
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.pylucene.search import PythonFieldComparator, PythonFieldComparatorSource
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.search import NumericRangeQuery
from org.apache.lucene.util import Version
from org.apache.lucene.search import Sort
from org.apache.lucene.search import SortField
from org.apache.lucene.queryparser.classic import QueryParserBase
from org.apache.lucene.queryparser.classic import MultiFieldQueryParser
from org.apache.lucene.search import BooleanClause
from socket import *


urls = ('/', 'index', '/im', 'index_img', '/s', 'text', '/i', 'image')


def dump(lst):
    fp = open("lst.utf8", "w")
    fp.write(json.dumps(lst, ensure_ascii=False))
    fp.close()


render = web.template.render('templates')  # your templates

login = form.Form(
    form.Textbox('keyword'),
    form.Button('香香一下'),
)


def func(command):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()

    STORE_DIR = "index_tb_new"

    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    query = QueryParser(Version.LUCENE_CURRENT, 'name', analyzer).parse(command)
    scoreDocs = searcher.search(query, 50).scoreDocs
    results = []
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        # shop perfumer xssd_comments name img url mid price sales comments 
        # rate place scents former xssd_name post xssd_url brand tune last
        shop=doc.get('shop')
        name=doc.get('name')
        img=doc.get('img')
        url = doc.get('url')
        post=doc.get('post')
        sales=doc.get('sales')
        comments=doc.get('comments')
        place=doc.get('place')
        price=doc.get('price')


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
        dump(data)
        # print(result['context'])
        results.append(data)
    return results


def func_img(command):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()

    STORE_DIR = "img_index"

    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

    command_dict = parseCommand(command)
    querys = BooleanQuery()

    for k, v in command_dict.iteritems():
        query = QueryParser(Version.LUCENE_CURRENT, k, analyzer).parse(v)
        querys.add(query, BooleanClause.Occur.MUST)
    scoreDocs = searcher.search(querys, 50).scoreDocs
    results = []
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        title = doc.get('title')
        url = doc.get('url')
        imgurl = doc.get('imgurl')

        result = {}
        result['url'] = url
        result['imgurl'] = imgurl
        result['title'] = title
        dump(result)
        # print(result['context'])
        results.append(result)
    return results




class index:
    def GET(self):
        f = login()
        return render.url_formtest(f)


class text:
    def GET(self):
        f = login()
        user_data = web.input()
        a = func(user_data.keyword)
        b = user_data.keyword
        num=len(a)
        return render.result(b,a,f,num)

class index_img:
    def GET(self):
        f = login()
        return render.formimg(f)

class image:
    def GET(self):
        user_data = web.input()
        a = func_img(user_data.keyword)
        b = user_data.keyword
        return render.result_img(a, b)


if __name__ == "__main__":
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    vm_env = lucene.initVM()
    app = web.application(urls, globals())
    app.run()
    del searcher
