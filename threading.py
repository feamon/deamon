#!/usr/bin/env python
#encoding: utf-8

import threading2
from time import sleep,ctime
loops = [4,2]

class MyThread(threading2.Thread):
    def __init__(self,func,args,name=''):
        threading2.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)

def loop(nloop,nsec):
    print 'start loop', nloop,'at:', ctime()
    sleep(nsec)
    print 'loop', nloop,'done at:',ctime()

def main():
    print 'starting at:',ctime()
    threads = []
    nloops = range(len(loops))

    for i in  nloops:
        t = MyThread(loop, (i,loops[i]),
             loop.__name__)
        threads.append(t)

        for i in nloops:
            threads[i].start()

        for i in nloops:
            threads[i].join()

            print 'all done at:',ctime()

if __name__ == '__main__':
    main()