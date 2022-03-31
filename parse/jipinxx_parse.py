#!/usr/bin/python
# -*- coding:UTF-8 -*-
# 文件名:jipinxx_parse.py
# 创建日期:2022/3/23 13:58
# 作者:XU
# 联系邮箱:iswongx@163.com

import re
#解析 www.jipinxx.com

def jipinxx_par(data,dict,dict_details):

    author = re.findall('<div id="info">.*?<strong>(.*?)</strong>', data, re.S)
    if author:
        dict_details['author'] = author[0]
    else:
        dict_details['author'] = ''
    description = re.findall('<div id="list">.*?<p>(.*?)</p>', data, re.S)
    if description:
        dict_details['describe'] = description[0].strip().replace('\r\n', '')
    else:
        dict_details['describe'] = ''
    dict_details['protagonist'] = ''
    tittle = re.findall('<div id="info">.*?<h1>(.*?)</h1>', data, re.S)
    if tittle:
        dict_details['tittle'] = tittle[0].strip()
    else:
        dict_details['tittle'] = ''
    dict['details'] = dict_details