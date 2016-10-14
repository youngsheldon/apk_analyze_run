#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-09-09 09:40:09
# @Last Modified by:   anchen
# @Last Modified time: 2016-09-09 11:32:05
import time 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ApkDecodeLogHandler(object):
    """docstring for ApkDecodeLogHandler"""
    def __init__(self, inpath, outpath, apk_md5):
        self.date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        self.inpath = inpath
        self.outpath = outpath
        self.apk_md5 = apk_md5

    def LogHandler(self):
        list1=[]
        f = open(self.inpath)
        for i in f:
            if 'INFO' in i or 'WARN' in i or 'ERROR' in i:
                if 'INFO' in i:
                    v = '[' + self.date + ' ' + i[0:8] + ']' + ' ' + '[' + 'INFO' + ']' + ' ' + i[17:]
                    list1.append(v)
                if 'WARN' in i:
                    v = '[' + self.date + ' ' + i[0:8] + ']' + ' ' + '[' + 'WARN' + ']' + ' ' + i[17:]
                    list1.append(v)
                if 'ERROR' in i:
                    v = '[' + self.date + ' ' + i[0:8] + ']' + ' ' + '[' + 'ERROR' + ']' + ' '+ i[17:]
                    list1.append(v)
        f.close()
        list1[0] = list1[0].strip() + '-begin to decode:' + self.apk_md5 + '.apk' + '\n'
        list1[-1] = list1[-1].strip() + '-finsh decode:' + self.apk_md5 + '.apk' + '\n'
        return list1

    def OutLog(self):
        f = open(self.outpath,'a+')
        ret = ''
        list1 = self.LogHandler()
        for i in list1:
            ret += i 
        f.write(ret)
        f.close()

inpath = sys.argv[1]
outpath = sys.argv[2]
apk_md5 = sys.argv[3]
obj = ApkDecodeLogHandler(inpath,outpath,apk_md5)
obj.OutLog()

