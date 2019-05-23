# -*- coding: UTF-8 -*-
import re
def perse(text):
    #使用正则表达式去除标点符号和换行符
    text = re.sub(r'[^\w ]', '',text)
    #转换为小写
    text = text.lower()
    #生成单词列表
    word_list = text.split(' ')
    #去除空白单词
    word_list = filter(None,word_list)

    #生成单词和词频的字典
    word_cnt = dict()
    for word in word_list:
        if word not in word_cnt:
            word_cnt[word] = 0
        word_cnt[word] += 1

    #按照词频排序
    sorted_word_cnt = sorted(word_cnt.items(),key=lambda kv: kv[1], reverse=True)
    return sorted_word_cnt

with open('/root/word.txt','r') as fin:
    text = fin.read()
word_and_freq = perse(text)
with open('/root/out.txt','w') as fout:
    for word, freq in word_and_freq:
        fout.write('{},{}\n'.format(word,freq))
