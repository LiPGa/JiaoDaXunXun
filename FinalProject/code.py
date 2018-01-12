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
from dHash import *

urls = ('/', 'index', '/im', 'Upload', '/s', 'text', '/i', 'index_img',
    '/perfumer','perfumer','/former','former','/mid','mid','/last','last','/scent','scent',
    '/brand','brand','/note','note','/c','cross_index','/cross','cross','/bs','bs','/brsc','brsc',
    '/sp','price','/formnote','formnote','/formsc','formsc',
    '/formbr','formbr','/formde','formde','/formfo','formfo','/formmi','formmi','/formla','formla',
    '/np','nameprice','/ns','namesales','/nst','namestandard','/nr','namerate','/pr','pr')


class Upload:
    def POST(self):
        x = web.input(myfile={})
        filedir = '' # change this to the directory you want to store the file in.
        if 'myfile' in x: # to check if the file-object is created

            # filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
            filepath = x.myfile.filename
            if filepath[-3:] != 'jpg':
                return render.upload('') # putout errorinformation
            
            print filepath

            filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
            fout = open(filename,'wb')
            # fout = open(filedir +'/'+ filename,'wb') # creates the file where the uploaded file should be stored

            fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.

        search = x.myfile.file.read()
        a = func_img(filename)
            
            # infile = filedir +'/'+filename
            # outfile = infile + ".jpg"
            # im = cv2.imread(filedir +'/'+filename)
            # cv2.imwrite(outfile,im)

        return render.result_img(a)

def dump(lst):
    fp = open("lst.utf8", "w")
    fp.write(json.dumps(lst, ensure_ascii=False))
    fp.close()


render = web.template.render('templates')  # your templates

login = form.Form(
    form.Textbox('keyword'),
    form.Button('香香一下'),
)
login2 = form.Form(
    form.Textbox('Former'),
    form.Textbox('Mid'),
    form.Textbox('Last'),     
    form.Button('香香一下'),
)
login3 = form.Form(
    form.Textbox('Brand'),
    form.Textbox('Scents'),   
    form.Button('香香一下'),
)

def func_img(img):
    pklfile = open('dhash.pkl','rb')
    dhash = pickle.load(pklfile)
    res = match2(img,dhash)
    results =[]
    for r in res:
        name=r[0]
        print name
        result=func(name)
        for i in range(9):
            results.append(result[i])
    return results

def process(scoreDocs,searcher):
    results = []
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
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

        data.setdefault('xssd_name',doc.get('xssd_name'))
        data.setdefault('perfumer',doc.get('perfumer'))
        data.setdefault('tune',doc.get('tune'))
        data.setdefault('xssd_url', doc.get('xssd_url'))
        data.setdefault('brand',doc.get('brand'))
        data.setdefault('rate',float(doc.get('rate')))
        data.setdefault('xssd_comments',doc.get('comment'))
        if doc.get('former')!=None:
            former=doc.get('former')
            mid=doc.get('mid')
            last=doc.get('last')
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

def func(command):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    STORE_DIR = "index_tb_new"
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    query = QueryParser(Version.LUCENE_CURRENT, 'name', analyzer).parse(command)
    scoreDocs = searcher.search(query, 239).scoreDocs
    results=process(scoreDocs,searcher)
    return results

def func_perfumer(command):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()

    STORE_DIR = "index_tb_new"

    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    query = QueryParser(Version.LUCENE_CURRENT, "perfumer",analyzer).parse(command)
    scoreDocs = searcher.search(query, 233).scoreDocs
    results=process(scoreDocs,searcher)    
    return results

def func_former(command):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    STORE_DIR = "index_tb_new"
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

    query = QueryParser(Version.LUCENE_CURRENT, "former",analyzer).parse(command)
    scoreDocs = searcher.search(query, 299).scoreDocs
    results=process(scoreDocs,searcher)    
    return results

def func_mid(command):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    STORE_DIR = "index_tb_new"
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

    query = QueryParser(Version.LUCENE_CURRENT, "mid",analyzer).parse(command)
    scoreDocs = searcher.search(query, 212).scoreDocs
    results=process(scoreDocs,searcher)    
    return results
def func_note(command):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    STORE_DIR = "index_tb_new"
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

    query = QueryParser(Version.LUCENE_CURRENT, "tune",analyzer).parse(command)
    scoreDocs = searcher.search(query, 200).scoreDocs
    results=process(scoreDocs,searcher)    
    return results

def func_last(command):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    STORE_DIR = "index_tb_new"
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

    query = QueryParser(Version.LUCENE_CURRENT, "last",analyzer).parse(command)
    scoreDocs = searcher.search(query, 200).scoreDocs
    results=process(scoreDocs,searcher)    
    return results

def func_scent(command):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    STORE_DIR = "index_tb_new"
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

    query = QueryParser(Version.LUCENE_CURRENT, "scents",analyzer).parse(command)
    scoreDocs = searcher.search(query, 200).scoreDocs
    results=process(scoreDocs,searcher)    
    return results

def func_np(command):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    STORE_DIR = "index_tb_new"
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    query = QueryParser(Version.LUCENE_CURRENT, "name",
                            analyzer).parse(command)
    scoreDocs = searcher.search(query,50, Sort([SortField("price", SortField.Type.DOUBLE,False),SortField.FIELD_SCORE])).scoreDocs
    results=process(scoreDocs,searcher)    
    return results
def func_ns(command):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    STORE_DIR = "index_tb_new"
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    query = QueryParser(Version.LUCENE_CURRENT, "name",
                            analyzer).parse(command)
    scoreDocs = searcher.search(query, 50 , Sort([SortField("sales", SortField.Type.INT,True),SortField.FIELD_SCORE,
                                     SortField("price", SortField.Type.DOUBLE,False)])).scoreDocs
    results=process(scoreDocs,searcher)    
    return results

def func_nr(command):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    STORE_DIR = "index_tb_new"
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    query = QueryParser(Version.LUCENE_CURRENT, "name",
                            analyzer).parse(command)
    scoreDocs = searcher.search(query, 50 , Sort([SortField("rate", SortField.Type.DOUBLE,True)])).scoreDocs
    results=process(scoreDocs,searcher)    
    return results

def func_cross(former,mid,last):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    STORE_DIR = "index_tb_new"
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    query=former+' '+' '+mid+' '+last
    fields = ["former", "mid","last"]
    clauses = [ BooleanClause.Occur.SHOULD, BooleanClause.Occur.SHOULD,BooleanClause.Occur.SHOULD]
    parser = MultiFieldQueryParser(Version.LUCENE_CURRENT, fields, analyzer)
    parser.setDefaultOperator(QueryParserBase.AND_OPERATOR)
    query = MultiFieldQueryParser.parse(parser, query)

    scoreDocs = searcher.search(query, 200).scoreDocs
    results=process(scoreDocs,searcher)    
    return results

def func_brsc(brand,scents):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    STORE_DIR = "index_tb_new"
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    query=brand+' '+scents
    fields = ["xssd_name", "scents"]

    clauses = [ BooleanClause.Occur.SHOULD, BooleanClause.Occur.SHOULD,
        BooleanClause.Occur.SHOULD]
    parser = MultiFieldQueryParser(Version.LUCENE_CURRENT, fields, analyzer)
    parser.setDefaultOperator(QueryParserBase.AND_OPERATOR)
    query = MultiFieldQueryParser.parse(parser, query)
    
    scoreDocs = searcher.search(query, 200).scoreDocs
    results=process(scoreDocs,searcher)    
    return results

def func_brand(command):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    STORE_DIR = "index_tb_new"
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

    query = QueryParser(Version.LUCENE_CURRENT, "xssd_name",analyzer).parse(command)
    scoreDocs = searcher.search(query, 200).scoreDocs
    results=process(scoreDocs,searcher)    
    return results
def func_pr(name,low,high):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    STORE_DIR = "index_tb_new"
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    query = QueryParser(Version.LUCENE_CURRENT, "name",
                            analyzer).parse(name)

    scoreDocs = searcher.search(query, 1000 , Sort([SortField.FIELD_SCORE,
        SortField("price", SortField.Type.DOUBLE,False)])).scoreDocs

    results=[]
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        if float(doc.get('price')) >=float(low) and float(doc.get('price'))<float(high):
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

            data.setdefault('xssd_name',doc.get('xssd_name'))
            data.setdefault('perfumer',doc.get('perfumer'))
            data.setdefault('tune',doc.get('tune'))
            data.setdefault('xssd_url', doc.get('xssd_url'))
            data.setdefault('brand',doc.get('brand'))
            data.setdefault('rate',float(doc.get('rate')))
            data.setdefault('xssd_comments',doc.get('comment'))
            if doc.get('former')!=None:
                former=doc.get('former')
                mid=doc.get('mid')
                last=doc.get('last')
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
            print data
    return results

class index_img:
    def GET(self):
        f = login()
        return render.formimg(f)
   
class namesales:
    def GET(self):
        f = login()
        user_data = web.input()
        a = func_ns(user_data.keyword)
        b = user_data.keyword
        num=len(a)
        return render.result(b,a,f,num,'1')
class pr:
    def GET(self):
        f = login2()
        user_data = web.input()
        low = user_data.low
        high=user_data.high
        b=user_data.name
        a= func_pr(b,low,high)
        num=len(a)
        return render.result(b,a,f,num,'1')

class nameprice:
    def GET(self):
        f = login()
        user_data = web.input()
        a = func_np(user_data.keyword)
        b = user_data.keyword
        num=len(a)
        return render.result(b,a,f,num,'1')
class namerate:
    def GET(self):
        f = login()
        user_data = web.input()
        a = func_nr(user_data.keyword)
        b = user_data.keyword
        num=len(a)
        return render.result(b,a,f,num,'1')
class namestandard:
    def GET(self):
        f = login()
        user_data = web.input()
        a = func(user_data.keyword)
        b = user_data.keyword
        num=len(a)
        return render.result(b,a,f,num,'1')
class perfumer:
    def GET(self):
        f = login()
        user_data = web.input()
        a = func_perfumer(user_data.keyword)
        b = user_data.keyword
        num=len(a)
        file=open('perfumer_pic.txt','r')
        pic=''
        for line in file.readlines():
            target=line.split('\t')[0]
            if target==b:
                pic=line.split('\t')[1]
        return render.perfumer_result(b,a,f,num,'1',pic)
class former:
    def GET(self):
        f = login()
        user_data = web.input()
        a = func_former(user_data.keyword)
        b = user_data.keyword
        num=len(a)
        return render.result(b,a,f,num,'1')

class mid:
    def GET(self):
        f = login()
        user_data = web.input()
        a = func_mid(user_data.keyword)
        b = user_data.keyword
        num=len(a)
        return render.result(b,a,f,num,'1')
class last:
    def GET(self):
        f = login()
        user_data = web.input()
        a = func_last(user_data.keyword)
        b = user_data.keyword
        num=len(a)
        return render.result(b,a,f,num,'1')
class scent:
    def GET(self):
        f = login()
        user_data = web.input()
        a = func_scent(user_data.keyword)
        b = user_data.keyword
        num=len(a)
        return render.result(b,a,f,num,'1')
class note:
    def GET(self):
        f = login()
        user_data = web.input()
        a = func_note(user_data.keyword)
        b = user_data.keyword
        num=len(a)
        return render.result(b,a,f,num,'1')
class brand:
    def GET(self):
        f = login()
        user_data = web.input()
        a = func_brand(user_data.keyword)
        b = user_data.keyword
        num=len(a)
        return render.result(b,a,f,num,'1')
class price:
    def GET(self):
        f = login()
        user_data = web.input()
        a = func_note(user_data.keyword)
        b = user_data.keyword
        num=len(a)
        return render.result(b,a,f,num,'1') 

class cross:
    def GET(self):
        f = login2()
        user_data = web.input()
        a = func_cross(user_data.Former,user_data.Mid,user_data.Last)
        b = 'cross searching'
        num=len(a)
        return render.result(b,a,f,num,'3')
class brsc:
    def GET(self):
        f = login3()
        user_data = web.input()
        a = func_brsc(user_data.Brand,user_data.Scents)
        b = 'cross searching'
        num=len(a)
        return render.result(b,a,f,num,'2')

class index:
    def GET(self):
        f = login()
        return render.url_formtest(f)
class formbr:
    def GET(self):
        f = login()
        return render.formbr(f)
class formde:
    def GET(self):
        f = login()
        return render.formde(f)
class formfo:
    def GET(self):
        f = login()
        return render.formfo(f)
class formmi:
    def GET(self):
        f = login()
        return render.formmi(f)
class formla:
    def GET(self):
        f = login()
        return render.formla(f)
class formsc:
    def GET(self):
        f = login()
        return render.formsc(f)
class formnote:
    def GET(self):
        f = login()
        return render.formnote(f)
class formla:
    def GET(self):
        f = login()
        return render.formla(f)

class text:
    def GET(self):
        f = login()
        user_data = web.input()
        a = func(user_data.keyword)
        b = user_data.keyword
        num=len(a)
        return render.result(b,a,f,num,'1')

class cross_index:
    def GET(self):
        f = login2()
        return render.formcross(f)

class bs:
    def GET(self):
        f = login3()
        return render.formbs(f)

class index_img:
    def GET(self):
        f = login()
        return render.formimg(f)


if __name__ == "__main__":
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    vm_env = lucene.initVM()
    app = web.application(urls, globals())
    app.run()
    del searcher
