#encoding = utf-8
# coding=UTF-8
from random import  randrange,choice
from  string import  ascii_letters as lc
from sys import maxint
from time import ctime
import MySQLdb


tlds = ('com','edu','net','org','gov')
f = open("/home/fred/22.log",'w+')
for i in xrange(randrange(5,11)):
    dtint = randrange(2**32)
    dtstr = ctime(dtint)
    llen = randrange(4,8)
    login = ''.join(choice(lc) for j in range(llen))
    dlen = randrange(llen,13)
    dom = ''.join(choice(lc) for j in range(dlen))
    print >> f,'%s::%s@%s.%s::%d-%d-%d' % (dtstr, login, dom, choice(tlds), dtint,llen,dlen)
f.close()
vvv = []
eee = []
count = 0
f = open("/home/fred/22.log",'r')
for eachline in f :
    (week , wwedde) = eachline.split(' ', 1)

    if week == 'Fri':
        vvv.append(week)

    if week  == 'Mon':
        eee.append(week)
    #eee =[]
    #vvv =[]
    count +=1
f.close()
print '周五有%d,周六有%d 一共有%d' % (len(eee),len(vvv),count)


def file_line (filename):
    with open("/home/fred/22.log",'r') as f:
        lines = f.readlines()
        for n in range(0,200):
            lines[n]= lines[n].split(' ',1)

            return lines[n]


def mysql_write():

    lines = file_line('22.log')
    conn = MySQLdb.connect(user='root', passwd='123456', db='pycharmdatabases', use_unicode=True)
    cursor = conn.cursor()
    #cursor.execute('create table gendate (id int(3) primary key, number varchar(100))')
    for n in range(0,200):
        cursor.execute("insert into `gendate`( `id`,`number`) values (%s,%s)", [n+2,lines[n]])

    conn.commit()
    cursor.close()
    conn.close()
    print "finish"

if __name__ == '__main__':
    mysql_write()


