#encoding=utf-8
#words = ['cat', 'dog', 'man']
import itertools
f = open("/home/fred/组合.log",'w+')

words = [
   'Motorcross','Motorbike','Bicycle','Off-Road','Street Track','Glove','Masei','Helmet','M/L/XL','Breathable Mesh','Open Face','Protective'
]

for r in itertools.permutations(words):
    print >>f,''.join(r)