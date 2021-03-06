#!/usr/bin/python
# -*- coding:UTF-8 -*-
# 文件名:xsb_xs_parse.py
# 创建日期:2022/3/23 13:50
# 作者:XU
# 联系邮箱:iswongx@163.com

import re

#解析网址 https://www.xsb-xs.com/

def xsb_xs_par(data,dict,dict_details):

    author = re.findall('<div id="info">.*?<p>作.*?者：(.*?)</p>', data, re.S)
    if author:
        dict_details['author'] = author[0]
    else:
        dict_details['author'] = ''
    description = re.findall('<div class="intro">.*?<br>(.*?)<br>', data, re.S)
    if description:
        dict_details['describe'] = description[0].strip().replace('\r\n','')
    else:
        dict_details['describe'] = ''
    dict_details['protagonist'] = ''
    tittle = re.findall('<div class="book-text">.*?<h1>(.*?)</h1>',data,re.S)
    if tittle:
        dict_details['tittle'] = tittle[0].strip()
    else:
        dict_details['tittle'] = ''
    dict['details'] = dict_details