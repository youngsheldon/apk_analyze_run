#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-09-18 22:37:41
# @Last Modified by:   anchen
# @Last Modified time: 2016-09-19 09:53:00
import re
import Mylog
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def TextPattern(Context, StringToFind):
    pattern = re.compile(StringToFind)  
    results = pattern.findall(Context) 
    if results:
        print results[0]
        return results[0]
    else:
        return None

def TimeCouter(path):
    f= open(path,'r')
    content = f.read()
    f.close()
    time_begin_expr = r'.*- loading.*'
    time_end_expr = r'.*- finished with errors.*'
    begin_time = TextPattern(content, time_begin_expr)
    end_time = TextPattern(content, time_end_expr)
    if begin_time is not None and end_time is not None:
        t1_h = begin_time[0:2]
        t1_m = begin_time[3:5]
        t1_s = begin_time[6:8]

        t2_h = end_time[0:2]
        t2_m = end_time[3:5]
        t2_s = end_time[6:8]
        return 3600*(int(t2_h) - int(t1_h)) + 60*(int(t2_m) - int(t1_m)) + int(t2_s) - int(t1_s)
    else:
        return None 

path = sys.argv[1]
output_file = sys.argv[2]
md5 = sys.argv[3]

v = TimeCouter(path)
if v:
    log = Mylog.Mylog(output_file).getObject()
    log.info('decode ' + md5 + ' take -' + str(v) + '- Seconds' + '\r')

