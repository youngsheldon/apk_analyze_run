#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-10-13 10:39:41
# @Last Modified by:   anchen
# @Last Modified time: 2016-10-14 16:08:14
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class OutDataForDataBase(object):
    """docstring for OutDataForDataBase"""
    def __init__(self, apk_log_path, apk_tell_report_path, database_data_out_path):
        self.apk_log_path = apk_log_path
        self.apk_tell_report_path = apk_tell_report_path 
        self.database_data_out_path = database_data_out_path
        self.out_data_list = []

    def apk_updata_log_handle(self):
        f = open(self.apk_log_path,'r')
        content = f.read()
        f.close()
        l = content.split(',')
        datetime = l[0]
        url =l[1]
        apk_md5 = l[2].strip()
        self.out_data_list.append(apk_md5)
        self.out_data_list.append(url)
        self.out_data_list.append(datetime)

    def apk_telldata_handle(self):
        f = open(self.apk_tell_report_path,'r')
        content = f.read()
        f.close()
        l = content.split('|')
        apk_md5 = l[0]
        self.out_data_list.append(l[1:10]) 

    def run(self):
        out_str = ''
        self.apk_updata_log_handle()
        self.apk_telldata_handle()
        out_str += self.out_data_list[0] + '|'
        out_str += self.out_data_list[1] + '|'
        out_str += self.out_data_list[2] + '|'
        for item in self.out_data_list[3]:
            out_str += str(int(float(item))) + '|'
        print out_str[:-1] 
        f = open(self.database_data_out_path,'w+')
        f.write(out_str[:-1] + '\n')
        f.close()

    def get_content(self,path):
        f = open(path,'r')
        content = f.read()
        f.close()
        return content

    def clear_file(self,path):
        f = open(path,'w+')
        f.write('')
        f.close()

    def do_run(self):
        self.clear_file(self.database_data_out_path)
        content = self.get_content(self.apk_tell_report_path)
        if content:
            self.run()
        else:
            self.clear_file(self.database_data_out_path)

apk_log_path = sys.argv[1]
apk_tell_report_path = sys.argv[2]
database_data_out_path = sys.argv[3]
obj = OutDataForDataBase(apk_log_path,apk_tell_report_path,database_data_out_path)
obj.do_run()
