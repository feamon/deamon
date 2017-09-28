import random
import string
import redis

forSelect = string.ascii_letters + string.digits


def generate_code(count, length):
    for x in range(count):
        Re = ""
        for y in range(length):
            Re += random.choice(forSelect)
        print(Re)
if __name__ == '__main__':
    generate_code(200, 20)


import MySQLdb

import random
import string

import MySQLdb

#forSelect = string.ascii_letters + string.digits


def generate_code(count, length):
    for x in range(count):
        Re = ""
        for y in range(length):
            Re += random.choice(forSelect)
        yield Re


def save_code():
    conn = MySQLdb.connect(user='root', passwd='123456', db='pycharmdatabases')
    #cur.execute('USE ')
    cursor = conn.cursor()
    codes = generate_code(200, 20)
    for code in codes:
        cursor.execute("INSERT INTO `code`(`code`) VALUES(%s)", [code])
    conn.commit()
    cursor.close()




if __name__ == '__main__':
    save_code()
