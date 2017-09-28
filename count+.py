#-*- coding:utf-8 -*-
import re
ww = file("123.text","r")
count =0

for s in ww.readlines():
    dd = re.findall("yes",s)
    if len(dd) > 0:
        count = count + len(dd)

#print "search" +  str(count) +   "hello"
print "%s 一共 %d 是 %s" % ('search' ,int(count) , 'yes')

ww.close()
