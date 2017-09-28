
#-*- coding: utf-8 -*-
from random import Random
from hashlib import md5

from random import Random
from hashlib import md5
import xlwt
import xlrd
from xlutils.copy import copy
import os

#获取四位数值的salt 值
def create_salt(length = 4):
    salt = ''
    chars ='AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    len_chars = len(chars) - 1
    random = Random()
    for i in xrange(length):
        salt += chars[random.randint(0,len_chars)]
    return salt
def create_md5(pwd,salt):
    md5_obj = md5()
    md5_obj.update (pwd+salt)
    return md5_obj.hexdigest()


# 创建一个xls文件
book = xlwt.Workbook()
# 创建一个sheet
sheet = book.add_sheet('users', cell_overwrite_ok=True)
# 每列第一行写上列名
sheet.write(0, 0, 'username')
sheet.write(0, 1, 'salt')
sheet.write(0, 2, 'pwd')
# 生成user数量
count = 60000



# 第一个id
first_id = 10000
for i in xrange(count):
    current_id = str(first_id + i)
    salt = create_salt()
    pwd = create_md5(current_id, salt)
    sheet.write(i+1, 0, current_id)
    sheet.write(i+1, 1, salt)
    sheet.write(i+1, 2, pwd)
# 保存
book.save('/home/fred/users.xls')

#追加数据
rb =xlrd.open_workbook('/home/fred/users.xls')
wb = copy(rb)
sheet = wb.get_sheet(0)
sheet.write =(1,3,'didi')
os.remove('/home/fred/users.xls')
wb.save('/home/fred/users.xls2')

