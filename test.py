

# -*- coding: utf-8 -*-
import re
f = open("/home/fred/cihui.log",'w+')
word_filter=set()
with open('/home/fred/filtered_words.txt') as f:

    for w in f.readlines():
        word_filter.add(w.strip())

while True:
    s=input()
    if s == 'exit':
        break
    for w in word_filter:

        if w in s:
            s= s.replace(w,'*'*len(w))
print('s')