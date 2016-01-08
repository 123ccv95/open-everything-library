import fileinput
import pprint 
import requests
import json

import time
import sys
import pprint
sys.path.append('libs/Wikipedia/')# #git clone git@github.com:goldsmith/Wikipedia.git
import wikipedia

import codecs
import os.path
import time
import sys
import pprint
import results
import json
sys.path.append('libs/Wikipedia/')# #git clone git@github.com:goldsmith/Wikipedia.git


import wikipedia

import six

from urlparse import urlparse, urlunparse
import urllib, urllib2

import requests
import codecs
import os.path


seen = {
    'NASA Open Source Agreement.data' :1, # skip
    'NASA Open Source Agreement' :1, # skip
}

def WikipediaResult(n,d=None):
    n = n + ".data"
    if not d:
        saw(n)
    if n not in seen :
        saw(n)


# from http://stackoverflow.com/questions/3627793/best-output-type-and-encoding-practices-for-repr-functions
def stdout_encode(u, default='UTF8'):
  return u

import codecs

def saw(x):

    x = x.decode('utf-8')
    
    y = x.encode('ascii', 'ignore')
    if x not in seen :
        seen[x]=1
        print "saw", x

    if y not in seen :
        seen[y]=1
        print "saw", y

def saw2(x):

    #x = x.decode('utf-8')
    
    y = x.encode('ascii', 'ignore')
    if x not in seen :
        seen[x]=1
        print "saw", x

    if y not in seen :
        seen[y]=1
        print "saw", y

from filelock import FileLock

def dowp(x):
    x = x.replace("Category:Category:","Category:")
    print "loading from WP:" + x
    #return

    print( "#" + x)
    try :
        results = wikipedia.page(x)
        #d = pprint.pformat(results.content)
        #pprint.pprint(results.__dict__)
        #pprint.pprint(dir(results))
        o = {
            'content': results.content,
            'categories' : results.categories,
            #'coordinates' : results.coordinates(),
            'images' : results.images,
            'links' : results.links,
            'original_title' : results.original_title,
            'pageid' : results.original_title,
            'references' : results.references,
            'revision_id' :results.revision_id,
            #'section' :results.section,
            'sections' :results.sections,
            'summary' :results.summary,
            'title': results.title,
            'url' : results.url,
        }
        #pprint.pprint(o)
        d = json.dumps(o)
    except Exception as e:
        print "error:", e
        d = ""
    fname = "data/results_wikipedia_data.py"
    with FileLock("myfile.txt"):
        f = codecs.open(fname,mode="a", encoding="utf-8")        
        #f.write( "#" + x + "\n")
        x2 = x.replace("\"","\\\"") # quotex
        f.write(    "WikipediaResult(\"\"\"%s\"\"\",%s)\n" % (x2, d))
        f.close()
        
    print "zzz"
    time.sleep(1)

def wp(x):
    if  x + ".data" not in seen :
        print  "load Page:" + x
        saw2(x + ".data")
        #return # skip for now
        dowp(x)
    else:      
        return

def wp2(x): # ascii name
    if  x + ".data" not in seen :
        print  "load Page:" + x
        saw(x + ".data")
        #return # skip for now
        dowp(x)
    else:      
        return

   

def WikipediaResultSubcat(n,d):
        
    m = d['query']['categorymembers']
    if len(m) == 0:
        return

    if n not in seen :
        print  "Existing Cat head: " + n
        saw(n)
        wp2(n)
    
    for x in m:
        t =  x['title']
        wp(t)
        if  t not in seen :
            #print  "Existing Cat: " + t
            pass
        #seen[ t ] = 1
           
        saw2( 'Category:' + t)

def WikipediaResultPages(n,d):
    if n not in seen :
        #print  "Existing Cat head: " + n
        saw(n)
    for x in d['query']['categorymembers']:
        t =  x['title']
        if  t not in seen :
            #print  "new Page " + t
            pass
        
        wp(t)
        saw2( t)


def process(filename, prefix):
    #### sub file, name
    f = open(filename)
    c = ""
    count = 0
    for l in f.readlines():
        #l = f.read();
        if l.startswith("#"):
            next
        else:
            if prefix in l:
                if count > 0 : # dont eval first line
                    #print "Eval:" + c
                    #try:
                    d = eval (c)
                    #except Exception as e:
                    #    print c
                    #    raise e

                # reset
                count = count + 1
                c = l
            else:
                c = c + l
            
    f.close()
    
def categorymembers(cmtype,category):
    url='https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'list': 'categorymembers',
        'cmtype': cmtype,
        'cmlimit': 'max',
        'format': 'json',
        'cmtitle': category,
    }
    
    r = requests.get(url, params=params)
    t = r.text
    d = json.loads(t)
    return d

def pages(category):
    return categorymembers('page',category)

def subcat(category):
    return categorymembers('subcat',category)

def data(name,x,d):
    saw(name)
    fname = "data/results_%s.py" % name
    term = "WikipediaResult%s" % name   
    f = open(fname,"a")
    f.write("%s(\"\"\"%s\"\"\"," % (term,x))
    d = pprint.pformat(d)
    f.write(d)
    f.write( ")\n")
    f.close()  

def load(name):
    fname = "data/results_%s.py" % name
    term = "WikipediaResult%s" % name
    process(fname,term)

def search (x):
    data("Pages",x, pages(x))
    data("Subcat",x, subcat(x))

process("data/results_wikipedia_data.py", "WikipediaResult") # new
#pprint.pprint(seen)

# load the existing articles
process("data/results_wikipedia_data2.py", "WikipediaResult") # old
#pprint.pprint(seen)


load("Pages")
#pprint.pprint(seen)

load("Subcat")
#pprint.pprint(seen)

for line in fileinput.input():
    line = line.replace("\n","")
    c = "Category:"+line
    if c not in seen:
        print "new '%s'" % c
        search(c)
