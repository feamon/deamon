#-*- coding:utf-8 -*-
import uuid
import MySQLdb

def generateActivationCode(num):
    codeList = []
    for i in range(num):
        code = str(uuid.uuid4()).replace('-','').upper()
        while code in codeList:
            code = str(uuid.uuid4()).replace('-','').upper()
        codeList.append(code)

    return codeList

def storeInMysql(codeList):
    try:
        conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='123456',db="pycharmdatabases")
        cursor = conn.cursor()
    except BaseException as e:
        print(e)
    else:
        try:
            #cur.execute('CREATE DATABASE IF NOT EXISTS pycharmdatabases ')
            #cur.execute('USE pycharmdatabases')
            #cur.execute('''CREATE TABLE dongyatable (
            #             id INT NOT NULL AUTO_INCREMENT,
            #                code VARCHAR(32) NOT NULL,
            #                PRIMARY KEY(id)
            #            )''')
            for code in codeList:
                cursor.execute("INSERT INTO `dongyatable`(`code`) VALUES(%s)",[code])
                conn.commit()

        except BaseException as e:
            print(e)
    finally:

        #conn.commit()
        cur.close()
        conn.close()


if __name__ == '__main__':
    storeInMysql(generateActivationCode(200))
    print('OK!')