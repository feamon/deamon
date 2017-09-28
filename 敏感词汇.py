# -*- coding: utf-8 -*-
import re
word_filter=set()
f = open("/home/fred/cihui.log",'w+')
def read_file(filename):
    #L = []
    with open(filename,"r")as fp:
        for line in fp.readline():
            word_filter.add(line.strip())
   # return

while True:'.join(string)
 #   return patten


#def input_check(patten):
#   sentance =raw_input("please enter word:")
    #if string in L:

    # print sentance

    #else:
       # print 'Human Rights'

def main():
    filename = ("/home/fred/filtered_words.txt")
    word_filter=read_file(filename)
   # patten = get_patten(L)
   # input_check(patten)

if __name__ == '__main__':
    main()





