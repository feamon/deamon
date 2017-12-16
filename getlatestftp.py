import ftplib
import os
import socket

HOST = 'ftp.mozilla.org'
DIER = 'pub/mozilla.org/webtools'
FIEL = 'bugzilla-latest.tar.gz'

def main():
    try:
        f = ftplib.FTP(HOST)
    except (socket.error,socket.gaierror) as e:
        print 'Error : cannot reach "%s"' % HOST
        return
    print '**** Connected to host "%s"' % HOST

    try:
        f.login()
    except ftplib.error_perm:
        print 'ERROR: cannot login anonymously'
        f.quit()
        return
    print '**** Logged in as "anonymously"'

    try:
        f.cwd(DIER)
    except ftplib.error_perm:
        print 'ERROR:cannot cd to "%s"' % DIER
        return
    print '*** Changed to "%s" folder' %DIER
    try:
        f.retrbinary('RETR %s' % FIEL,open(FIEL,'wb').write)
    except ftplib.error_perm:
        print 'ERROR: cannot read file "%s"' % FIEL
        os.unlink(FIEL)
    else:
        print '*** Downloaded "%s" to CWD' % FIEL
    f.quit()
if __name__ == '__main__':
    main()
