#!/bin/env python
#-*-coding:utf-8-*-
import MySQLdb
import requests
import json
from influxdb import InfluxDBClient
import sys
import time
from gevent import monkey
import gevent
import urllib2
from gevent.pool import Pool
from gevent.threadpool import ThreadPool
from prettytable import PrettyTable 
import numpy as np
import pandas as pd
import datetime
reload(sys)  
sys.setdefaultencoding('utf8')

session = requests.Session()


weektime = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%V")

def query(sql,host,port):
    try:
        conn=MySQLdb.connect(host=host,user=user,passwd=passwd,port=int(port),connect_timeout=5,charset='utf8')
        cursor = conn.cursor()
        count=cursor.execute(sql)
        index=cursor.description
        result=cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception,e:
        return ([str(e)],'')

def get_slow_count_and_time(cluster,need_time):
    try:
        conn=MySQLdb.connect(host='data-mysql01.corp.cootek.com',user='boomdb',passwd='123456',port=3313,connect_timeout=5,charset='utf8')
        cursor = conn.cursor()
        sql = "select sum(time),sum(count) from boomdb.slowsql_info where cluster='%s' and update_time > %s" % (cluster,need_time)
        count=cursor.execute(sql)
        index=cursor.description
        result=cursor.fetchall()
        cursor.close()
        conn.close()
        return result[0][0],result[0][1]
    except Exception,e:
        print e
        return 0,0

def query_for_zabbix(sql,host,port):
    try:
        conn=MySQLdb.connect(host=host,user=user,passwd=passwd,port=int(port),connect_timeout=5,charset='utf8')
        cursor = conn.cursor()
        count=cursor.execute(sql)
        result=cursor.fetchall()
        cursor.close()
        conn.close()
        if count == 0:
            return ('N/A')
        else:
            return result[0]
    except Exception,e:
        return ([str(e)],'')

def get_qps_speed(instance):
    sql_now = 'select unix_timestamp(create_time),operation_count,transaction_count,slowsql_count from boomdb.mysql_performance_monitor where instance="%s" and TO_DAYS(NOW()) - TO_DAYS(create_time) = 0 limit 1;' % instance
    sql_lastweek = 'select unix_timestamp(create_time),operation_count,transaction_count,slowsql_count from boomdb.mysql_performance_monitor where instance="%s" and TO_DAYS(NOW()) - TO_DAYS(create_time) = 7 limit 1;' % instance
    result_now = query(sql_now, boomdbhost, boomdbport)
    result_lastweek = query(sql_lastweek, boomdbhost, boomdbport)
    if result_now == () or result_lastweek == ():
        qps,tps,slowqps = 'None','None','None'
    else:
        qps = (result_now[0][1] - result_lastweek[0][1])/(result_now[0][0] - result_lastweek[0][0])
        tps = (result_now[0][2] - result_lastweek[0][2])/(result_now[0][0] - result_lastweek[0][0])
        slowqps = (result_now[0][3] - result_lastweek[0][3])/(result_now[0][0] - result_lastweek[0][0])
    return qps,tps,slowqps

def get_cpu_status(instance):
    sql_hostid = "select hostid from zabbix.hosts where host='%s'" % instance
    hostid = query_for_zabbix(sql_hostid,zabbixhost,zabbixport)
    sql_itemid = "select itemid from zabbix.items where hostid='%s' and key_ = 'system.cpu.util[,idle]'" % hostid[0]
    itemid = query_for_zabbix(sql_itemid, zabbixhost, zabbixport)
    sql_cpu_status = "select min(value),avg(value) from zabbix.history where itemid = '%s' and clock > %s" % (itemid[0],int(time.time())-86400*7)
    cpu_status = query_for_zabbix(sql_cpu_status,zabbixhost,zabbixport)
    return cpu_status

def get_io_status(instance):
    sql_hostid = "select hostid from zabbix.hosts where host='%s'" % instance
    hostid = query_for_zabbix(sql_hostid,zabbixhost,zabbixport)
    sql_itemid = "select itemid from zabbix.items where hostid='%s' and key_ like 'iostat[sdb," % hostid[0] + '%util]\''
    itemid = query_for_zabbix(sql_itemid,zabbixhost,zabbixport)
    if itemid == 'N/A':
        sql_itemid = "select itemid from zabbix.items where hostid='%s' and key_ like 'iostat[sda," % hostid[0] + '%util]\''
        itemid = query_for_zabbix(sql_itemid, zabbixhost, zabbixport)
    if itemid == 'N/A':
        sql_itemid = "select itemid from zabbix.items where hostid='%s' and key_ like 'iostat[xvdb," % hostid[0] + '%util]\''
        itemid = query_for_zabbix(sql_itemid, zabbixhost, zabbixport)
    if itemid == 'N/A':
        sql_itemid = "select itemid from zabbix.items where hostid='%s' and key_ like 'iostat[xvda," % hostid[0] + '%util]\''
        itemid = query_for_zabbix(sql_itemid, zabbixhost, zabbixport)
    sql_io_status = "select max(value),avg(value) from zabbix.history where itemid = '%s' and clock > %s" % (itemid[0],int(time.time())-86400*7)
    io_status = query_for_zabbix(sql_io_status,zabbixhost,zabbixport)
    return io_status

def get_disk_status(instance):
    sql_hostid = "select hostid from zabbix.hosts where host='%s'" % instance
    hostid = query_for_zabbix(sql_hostid,zabbixhost,zabbixport)
    sql_itemid = "select itemid from zabbix.items where hostid='%s' and key_ = 'vfs.fs.size[/db,pfree]'" % hostid[0]
    itemid = query_for_zabbix(sql_itemid, zabbixhost, zabbixport)
    if itemid == 'N/A':
        sql_itemid = "select itemid from zabbix.items where hostid='%s' and key_ = 'vfs.fs.size[/,pfree]'" % hostid[0]
        itemid = query_for_zabbix(sql_itemid, zabbixhost, zabbixport)
    sql_disk_status = "select value from zabbix.history where itemid = '%s' order by clock desc limit 1" % itemid[0]
    disk_status = query_for_zabbix(sql_disk_status,zabbixhost,zabbixport)
    return disk_status

def get_mysql_instance():
    sql = "select distinct(instance),locate,`group`,comments,cluster from boomdb.mysql_instance_info where type != 'Bridge-Slave' and instance not in \
    ('beta03.corp.cootek.com:3306','eu-mysql-rds-slave:3306','eu-mysql-rds-master:3306','gaia-docker02.corp.cootek.com:3306','eza03.uscasv2.cootek.com:3306','stream04.uscasv2.cootek.com:3306','ops02.corp.cootek.com:3306') \
    and instance not like 'mmm02.corp%' and instance not like '%redis%' and instance not like '%http%' and instance not like '%ime%' and instance not like '%guldan%'"
    result = query(sql, boomdbhost, boomdbport)
    return result

def monitor(i):
    try:
        target_host = i[0].split(":")[0]
        target_port = i[0].split(":")[1]
        location = i[1]
        sql = "SELECT sum(`DATA_LENGTH`/(1024*1024*1024)) AS `DATA(G)`,sum(`INDEX_LENGTH`/(1024*1024*1024)) AS `INDEX(G)`,sum((INDEX_LENGTH + DATA_LENGTH)/(1024*1024*1024)) AS `TOTAL(G)` FROM  INFORMATION_SCHEMA.TABLES WHERE ENGINE='InnoDB';"
        result = query(sql, target_host, target_port)
        result_qps = get_qps_speed(i[0])
        cpu_status = get_cpu_status(target_host)
        if cpu_status[0] is None:
            cpu_max = 'None'
            cpu_avg = 'None'
        else:
            cpu_max = 100 - int(cpu_status[0])
            cpu_avg = 100 - int(cpu_status[1])
        io_status = get_io_status(target_host)
        io_max = io_status[0]
        io_avg = io_status[1]
        disk_status = get_disk_status(target_host)
        if disk_status[0] is None:
            disk_free = 'None'
        else:
            disk_free = disk_status[0]
        return i[0],disk_free,cpu_max,cpu_avg,io_max,io_avg,i[4]
    except Exception,e:
        return e
        print e

if __name__ == '__main__':
    start_time = time.time()
    user = 'boomdb'
    passwd = '123456'
    boomdbhost = 'data-mysql01.corp.cootek.com'
    boomdbport = 3313
    zabbixhost = 'ops-mysql01.corp.cootek.com'
    zabbixport = 3306
    monkey.patch_all()
    pool = ThreadPool(32)
    gevents = []
    instances = get_mysql_instance()
    for i in instances:
        gevents.append(pool.spawn(monitor, i))
    pool.join()
    #TABLE = PrettyTable(["Instance Name","LOCATE", "DATA(G)", "INDEX(G)", "TOTAL(G)","QPS","TPS","SLOW-QPS",'Project Team',"CPU_MAX","CPU_AVG","IO_MAX","IO_AVG","DISK_MAX","DISK_AVG",'Comments'])
    #TABLE.align["Instance Name"] = "l"# Left align Instance name
    #TABLE.padding_width = 1
    data_list = []
    for x in gevents:
        data_list.append(x.value)
        #print x.value
        #TABLE.add_row(x.value)
    #(datetime.datetime.now()+datetime.timedelta(days=-7)).strftime("%W")
    dbgroup_list = []
    dbgroup_dic = {}


    try:
        for d in data_list:
            d = list(d)
            if d[6] in dbgroup_list:
                old_data = dbgroup_dic[d[6]]
                new_data = old_data
                if type(d[1]) == int or type(d[0]) == float:
                    disk_free = float(d[1])
                else:
                    disk_free = 'None'
                    cpu_max = d[2]
                    cpu_avg = d[3]
                    io_max = d[4]
                    io_avg = d[5]
                if new_data[0] > disk_free:
                    new_data[0] = disk_free
                if new_data[1]  < cpu_max:
                    new_data[1]  = cpu_max
                if new_data[2]  < cpu_avg:
                    new_data[2] = cpu_avg
                if new_data[3] < io_max:
                    new_data[3] = io_max
                if new_data[4] < io_avg:
                    new_data[4] = io_avg
                dbgroup_dic[d[6]] = new_data
            else:
                dbgroup_list.append(d[6])
                new_dic = {}
                dbgroup = d[6]
                new_dic[dbgroup] = d[1:-1]
                dbgroup_dic.update(new_dic)
    except Exception,e:
        print e,d

    sum_data = []
    for i in dbgroup_dic:
        new_data_dic = dbgroup_dic[i]
        last_week_time=(datetime.datetime.now()+datetime.timedelta(days=-7)).strftime("%Y-%m-%d")
        sum_time,sum_count = get_slow_count_and_time(i,last_week_time)
	if sum_time == 'None' or sum_time is None:
	    sum_time = 0
	print sum_time
	sum_time = int(sum_time/3600)
	if new_data_dic[0] != 'N':
	    print new_data_dic[0]
            new_data_dic[0] = 100 - new_data_dic[0]
        new_data_dic.append(i)
        new_data_dic.append(sum_time)
	if i != 'None' or i is not None:
            sum_data.append(new_data_dic)

    data_save = pd.DataFrame(sum_data,columns=["DISK_USED(%)","CPU_MAX(%)","CPU_AVG(%)","IO_MAX(%)","IO_AVG(%)","Cluster","慢查询总时间（小时）"])
    save_file = '/opt/scripts/mysql_report_weekly/mysql_report_' + weektime + '.csv'
    data_save.sort_values(by=["DISK_USED(%)"]).to_csv(save_file,na_rep='None',encoding='utf_8_sig')
    print time.time() - start_time
