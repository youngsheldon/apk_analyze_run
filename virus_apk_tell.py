#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-09-27 12:05:28
# @Last Modified by:   anchen
# @Last Modified time: 2016-10-14 17:33:52
import re 
import os 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

permis_grade_fir = ['PROCESS_OUTGOING_CALLS','READ_CALENDAR','READ_CONTACTS','READ_HISTORY_BOOKMARKS','READ_SMS','RECEIVE_SMS','SEND_SMS','WRITE_SMS','CALL_PHONE','BROADCAST_SMS','BROADCAST_STICKY','BROADCAST_WAP_PUSH','READ_LOGS','WRITE_CONTACTS','WRITE_CALL_LOG']
permis_grade_sec = ['KILL_BACKGROUND_PROCESSES','MODIFY_PHONE_STATE','READ_PHONE_STATE','REBOOT','RECEIVE_BOOT_COMPLETED','RECEIVE_WAP_PUSH','WRITE_SECURE_SETTINGS','WRITE_SETTINGS','BIND_DEVICE_ADMIN','DELETE_PACKAGES','INSTALL_PACKAGES','WRITE_EXTERNAL_STORAGE','GET_TASKS','RESTART_PACKAGES','CHANGE_NETWORK_STATE']
action_grade_fir = ['android.intent.action.NEW_OUTGOING_CALL','android.provider.Telephony.SMS_RECEIVED' ,'android.provider.Telephony.SMS_RECEIVED_2','android.provider.Telephony.GSM_SMS_RECEIVED','android.net.conn.CONNECTIVITY_CHANGE','android.provider.Telephony.SMS_DELIVER','android.intent.action.SEND','android.intent.action.SENDTO','android.intent.action.RESPOND_VIA_MESSAGE']
action_grade_sec = ['android.intent.action.PACKAGE_RESTARTED','android.intent.action.BOOT_COMPLETED','android.media.RINGER_MODE_CHANGED','android.intent.action.DELETE','android.app.action.DEVICE_ADMIN_ENABLED','android.intent.action.PACKAGE_ADDED','android.intent.action.PACKAGE_REPLACED','android.intent.action.PACKAGE_INSTALL','android.intent.action.ACTION_PACKAGE_CHANGED','android.intent.action.SIG_STR']

sender = ['Key14','Key15']
sendExe = ['Key08','Key10']
getContent = ['Key02','Key03','Key04','Key06']
badBehavior = ['Key01','Key05','Key12','Key13']

class VirusApkAnalyze(object):
    """docstring for VirusApkAnalyze"""
    def __init__(self, apk_md5, codeblock_path, act_permis_path, tell_out_path):
        self.apk_md5 = apk_md5
        self.codeblock_path = codeblock_path
        self.act_permis_path = act_permis_path
        self.tell_out_path = tell_out_path
        self.permis_list = []
        self.act_list = []
        self.permis_act_list_generator()
        self.item_couter_list = []

    def add2list(self,item):
        self.item_couter_list.append(item)

    def item_couter(self,content,detectItem):
        couter = 0 
        for item in detectItem:
            ret = content.find(item)
            if ret is not -1:
                couter += 1
        return couter

    def permis_act_list_generator(self):
        f = open(self.act_permis_path,'r')
        for line in f:
            tag = int(line.split('|')[1].strip())
            value = line.split('|')[2].strip()
            if tag == 1:
                self.permis_list.append(value)
            else:
                self.act_list.append(value)
        f.close()

    def codeblock_evaluation(self):
        f = open(self.codeblock_path,'r')
        content = f.read()
        f.close()
        senderCouter = self.item_couter(content,sender)
        print 'senderCouter=' + str(senderCouter)
        self.add2list(senderCouter)
        sendExeCouter = self.item_couter(content,sendExe)
        print 'sendExeCouter=' + str(sendExeCouter)
        self.add2list(sendExeCouter)
        getContentCouter = self.item_couter(content,getContent)
        print 'getContentCouter=' + str(getContentCouter)
        self.add2list(getContentCouter)
        badBehaviorCouter = self.item_couter(content,badBehavior)
        print 'badBehaviorCouter=' + str(badBehaviorCouter) 
        self.add2list(badBehaviorCouter)
        if senderCouter != 0 and sendExeCouter != 0 and getContentCouter != 0:
            ret1 = 50.0 + 10.0 * ((senderCouter + sendExeCouter + getContentCouter)/8.0)
        else:
            ret1 = 0
        ret2 = 10.0 * (badBehaviorCouter/4.0)
        sum = ret1 + ret2 
        return ret1 + ret2 

    def permis_evaluation(self):
        permis_grade_fir_couter = 0 
        permis_grade_sec_couter = 0 
        for item in self.permis_list:
            if item in permis_grade_fir:
                permis_grade_fir_couter += 1
            if item in permis_grade_sec:
                permis_grade_sec_couter += 1
        print 'permis_grade_fir_couter=' + str(permis_grade_fir_couter)
        print 'permis_grade_sec_couter=' + str(permis_grade_sec_couter)
        self.add2list(permis_grade_fir_couter)
        self.add2list(permis_grade_sec_couter)
        return 10.0*permis_grade_fir_couter/15.0 + 10.0*permis_grade_sec_couter/15.0  

    def act_evaluation(self):
        action_grade_fir_couter = 0 
        action_grade_sec_couter = 0 
        for item in self.act_list:
            if item in action_grade_fir:
                action_grade_fir_couter += 1
            if item in action_grade_sec:
                action_grade_sec_couter += 1
        print 'action_grade_fir_couter=' + str(action_grade_fir_couter)
        print 'action_grade_sec_couter=' + str(action_grade_sec_couter)
        self.add2list(action_grade_fir_couter)
        self.add2list(action_grade_sec_couter)
        return 5.0*action_grade_fir_couter/9.0 + 5.0*action_grade_sec_couter/10.0  

    def virus_apk_evaluation(self):
        value = self.codeblock_evaluation() + self.permis_evaluation() + self.act_evaluation()
        self.add2list(value)
        print 'virus_probility' + ':' + str(value)
        return value 
    
    def tell_out(self):
        f = open(self.tell_out_path,'w+')
        f.write(self.apk_md5 + '|')
        for item in self.item_couter_list:
            f.write(str(item) + '|')
        f.write('\n')
        f.close()

    def run(self):
        self.virus_apk_evaluation()
        self.tell_out()

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
        self.clear_file(self.tell_out_path)
        codeblock_content = self.get_content(self.codeblock_path)
        act_permis_content = self.get_content(self.act_permis_path)
        if codeblock_content and act_permis_content:
            self.run()
        else:
            self.clear_file(self.tell_out_path)
            print 'the file content is None ,stop virus_apk_tell.py'

apk_md5 = sys.argv[1]
codeblock_path = sys.argv[2]
act_permis_path = sys.argv[3]
tell_out_path = sys.argv[4]

obj = VirusApkAnalyze(apk_md5,codeblock_path,act_permis_path,tell_out_path)
obj.do_run()