# -*- coding: utf-8 -*-
import re

def counter (string):
    words = re.findall(r'[a-zA-z]+(\'[a-zA-Z]+|\b)',string)
    acount = len(words)
    return str(acount)

def file_read(filename):
    with open(filename,'r') as fp:
        asdsds = fp.read()
        return asdsds

if __name__== '__main__':
    string = file_read('/home/fred/gitgub.txt')
    resturt = counter(string)
    print  'There are', resturt, 'words in this article.'

    print  '这篇文章中有' + resturt + '个英文单词'