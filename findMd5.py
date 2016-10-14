#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-09-13 11:27:04
# @Last Modified by:   anchen
# @Last Modified time: 2016-09-13 14:52:17
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def find(md5):
    f = open('md5_log.txt','r')
    content = f.read()
    f.close()
    if md5 in content:
        sys.exit(1)
    else:
        sys.exit(0)

md5=sys.argv[1]
find(md5)


