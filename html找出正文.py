encoding = utf-8
#coding = utf-8
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


import re
import glob
import urllib2

from pyquery import PyQuery as pq
from lxml import etree
f = open("/home/fred/2233.log",'w+')

headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

def get_html (url):
    url =urllib2.Request('http://jimmy66.com/164.html',headers=headers)
    html = urllib2.urlopen(url).read()
    return html

def get_content(html):
    match = re.search(r'<div class="content">([^$]*)<div class="article-copyright">',html)
    content = match.group(1)
    return content
def get_result (content):
    content =content.decode('utf-8')
    jp =pq(content)
    l = jp('p')
    result = []
    for string in l:
        result.append(pq(string).text())
    return result

def main():
    url = 'http://jimmy66.com/164.html'
    html = get_html(url)
    content = get_content(html)
    result = get_result(content)
    for line in result:
        print >> f,'%s'  % (line)



if __name__ == '__main__':

    main()

f.close()



