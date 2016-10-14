#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-08-23 17:24:54
# @Last Modified by:   anchen
# @Last Modified time: 2016-10-14 15:29:04
import os
import re
import sys
import time
import Mylog
reload(sys)
sys.setdefaultencoding('utf-8')

dict = {'Key01':'setComponentEnabledSetting','Key02':'getDeviceId','Key03':'Phone',
'Key04':'CallLog','Key05':'DevicePolicyManager','Key06':'sms','Key07':'connectivity','Key08':'mail','Key09':'getSharedPreferences','Key10':'sendTextMessage','Key11':'createFromPdu','Key12':'ACTION_CHANGE_DEFAULT','Key13':'abortBroadcast','Key14':'@','Key15':'1'}

class Analyze(object):
    """docstring for Analyze"""
    def __init__(self, FilePath, apk_md5, output_file, log_file, temp_out_file):
        self.output_file = output_file
        self.FilePath = FilePath 
        self.apk_md5 = apk_md5
        self.log_file = log_file
        self.key = ''
        self.filepath = ''
        self.line_index = ''
        self.code_content = ''
        self.log = Mylog.Mylog(self.log_file).getObject()
        self.print_flag = 0
        self.temp_content = ''
        self.temp_out_file = temp_out_file

    def clear(self):
        self.log.info('clear')
        self.filepath = ''
        self.line_index = ''
        self.code_content = ''

    def enablePrint(self):
        self.print_flag = 1

    def getRegularExpression(self):
        self.log.info('getRegularExpression')
        expr_dict={}
        f=open('setting/config.ini','r')
        for i in f:
            if 'Key' in i:
                ret=i.split('\n')
                ret1=ret[0].split('=')
            expr_dict[ret1[0]] = ret1[1]
        f.close()
        expr_list=sorted(expr_dict.iteritems(),key = lambda asd:asd[0],reverse = False)
        return expr_list

    def OutPutReport(self):
        self.log.info('OutPutReport')
        f = open(self.output_file, 'a+')
        out = self.apk_md5 + '|' + self.key + '|' + self.filepath + '|' + self.line_index + '|' + self.code_content + '\n'
        f.write(out)
        f.close()
        self.temp_content += out 

    def out_temp_file(self):
        f = open(self.temp_out_file,'w+')
        f.write(self.temp_content)
        f.close()

    def GetFilePathList(self, rootDir):
        self.log.info('GetFilePathList')
        FilePathList=[]
        for root,dirs,files in os.walk(rootDir):
            for filespath in files:
                FilePathList.append(os.path.join(root,filespath))
        return FilePathList

    def GetCodeBlockFromJavaSouce(self, Context, StringToFind):
        ret = Context.find(dict[self.key])
        if ret is not -1:
            pattern = re.compile(StringToFind)  
            results = pattern.findall(Context) 
            return results
        else:
            return None

    def FindTarStringLocationInFile(self, file, TarString):
        self.log.info('FindTarStringLocationInFile')
        line_num = 0
        ContextToSave = ''
        f=open(file,'r')
        for line in f:
            line_num+=1
            ret = self.GetCodeBlockFromJavaSouce(line,TarString)
            if ret and "CONTACT javamail@sun.com" not in line and 'android' not in file:
                ContextToSave+= file +':' + str(line_num)+'\r'+line+'\r'
                self.filepath = file
                self.line_index = str(line_num)
                self.code_content = line.strip()
                break 
        if self.print_flag:
            print ContextToSave
        f.close()

    def FindTarString(self,TarString):
        self.log.info('FindTarString')
        list=self.GetFilePathList(self.FilePath)
        for l in list:
            if 'android' not in l and 'javax' not in l and 'res' not in l and '.java' in l:
                f=open(l,'r')
                Context=f.read()
                f.close()
                ret=self.GetCodeBlockFromJavaSouce(Context,TarString)
                if ret:
                    self.FindTarStringLocationInFile(l,TarString)
                    break 

    def run(self):
        self.log.info('run -begin to find key codeblock in '+ self.apk_md5 + '.apk' + ' source')
        expr_list = self.getRegularExpression()
        for l in expr_list:
            self.key = l[0]
            if self.print_flag:
                print l[0]
            self.FindTarString(l[1])
            if self.code_content is not '':
                self.OutPutReport()
            self.clear()
        self.out_temp_file()

    def clear_file(self,path):
        f = open(path,'w+')
        f.write('')
        f.close()

    def do_run(self):
        self.clear_file(self.temp_out_file)
        path_exits = os.path.exists(self.FilePath)
        if path_exits:
            self.run()
        else:
            self.clear_file(self.temp_out_file)

# tarpath = "2ce58586fc2b0ef6dccda83d1e6ca030/"
# apk_md5 = "2ce58586fc2b0ef6dccda83d1e6ca030"
# outPutfileName = "result/output.txt"
# log_file = "sort.log"

tarpath = sys.argv[1]
apk_md5 = sys.argv[2]
outPutfileName = sys.argv[3]
log_file = sys.argv[4]
temp_out_file = sys.argv[5]

start = time.clock()
obj = Analyze(tarpath,apk_md5,outPutfileName,log_file,temp_out_file)
obj.do_run()
obj.log.info('finish find key codeblock in '+ apk_md5 + '.apk' + ' source')
end = time.clock()
print 'Running time: %s Seconds'%(end-start)

mylog = Mylog.Mylog('log/decode_time.log').getObject()
mylog.info('sortCode ' + apk_md5 + ' Running time: %s Seconds'%(end-start) + '\r')