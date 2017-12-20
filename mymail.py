from smtplib import SMTP
from poplib import POP3
from time import sleep


SMTPSVR = 'smtp.python.is.cool'
POP3SVR = 'pop.python.is.cool'

who = 'deamon@python.is.cool'
body= '''\
From: %(who)s
To: %(who)s
Subject: test msg

Hello World!
'''% {'who':who}

sendSvr = SMTP(SMTPSVR)
errs = sendSvr.sendmail(who, [who], origMsg)
sendSvr.quit()
assert len(errs) ==0,errs
sleep(10)

recvSvr = POP3(POP3SVR)
recvSvr.user('deamon')
recvSvr.pass_('123455')
rsp,msg,siz = recvSvr.retr(recvSvr.stat()[0])

sep = msg.index('')
recvBody = msg[sep+1:]
assert origBody == recvBody

