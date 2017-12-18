# -*- coding: utf-8 -*-
# Script Name		: getfirstnntp.py

# Author		: Deamon
# Created		: 18 Dec 2017
# Version		: 1.0
# Description	: 下载并显示Python新闻组comp.lang.python中最新一篇文章前20个'有意义'的行

#!/usr/bin/python
import nntplib
import socket

HOST = 'your.nntp.server'
GRNM = 'camp.lang.pythom'
USER = 'deamon'
PASS = 'youllnerverguess'

def main():

    try:
        n = nntplib.NNTP(HOST)
    except socket.gaierror as e:
        print 'ERROR: cannot reach host "%s"' % HOST
        print '     (%s)' % eval (str(e))[1]
        return
    except nntplib.NNTPPermanentError as e:
        print 'ERROR : access denied on "%s"' % HOST
        print '     (%s)' %str(e)
        return
    print '**** Connected to host "%s"' %HOST

    try:
        rsp, ct, fst, lst, grp = n.group(GRNM)
    except nntplib.NNTPPermanentError as ee:
        print 'ERROE : cannot load grpup "%s"' % GRNM
        print '   ("%s")' % str(e)
        print ' Server may require authentication'
        print ' Uncomment/edit login line above'
        n.quit()
        return
    except nntplib.NNTPTemporaryError as ee:
        print ' ERROR : group "%s"' % GRNM
        print '    ("%s")' % str(e)
        n.quit()
        return
    print '***** Found newsgroup "%s"' % GRNM

    rng = '%s-%s' % (lst, lst)
    rsp, frm = n.xhdr('from', rng)
    rsp, sub = n.xhdr('subjec', rng)
    rsp, dat = n.xhdr('date', rng)
    print '''*** Found last article(#%s):

    From: %s
    Subject: %s
    Date: %s
    ''' % (lst, frm[0][1], sub[0][1], dat[0][1])


def displayFirst20(data):
    'Display First 20 lines'
    count = 0
    lines = (line.rstrip() for line in data)
    lastBlank = True
    for line in lines:
        if line:
            lower = line.lower()
            if (lower.startswith('>') and not
            lower.startswith('>>>')) or \
            lower.startswith('|') or \
            lower.startswith('in article') or \
            lower.endswith('writes:') or \
            lower.endswith('wrote:'):
                continue
        if not lastBlank or (lastBlank and line):
           print '%s' % line
        if line:
            count += 1
            lastBlank = False
        else:
             lastBlank = True
       if count == 20:
          break


def main():
   NNTPClient()
   DisplayFirst20()


if __name__ == '__main__':
    main()