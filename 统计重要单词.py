#coding = utf-8
# -*- coding: utf-8 -*-

import re


def list1(string):
    words = re.findall(r'[a-zA-Z]+\b',string)
    return words


def file_read(filename):
    with open(filename,'r') as fp:
        dongya = fp.read()
        return dongya



def most_word_number(word_list):
    str_dict={}
    for items in word_list:
        if items in str_dict:
            str_dict[items] += 1
        else:

            str_dict[items] = 1


    str_dict = {str_dict[key]:key for key in str_dict}
    return (max(str_dict),str_dict[max(str_dict)])




if __name__ == '__main__':


    string = file_read('/home/fred/gitgub.txt')
    words = list1(string)
    times,word = most_word_number(words)
    print '出现最多的单词为' + str(word) + '出现了' + str(times) + '次'



