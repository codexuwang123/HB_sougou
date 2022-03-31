#!/usr/bin/python
# -*- coding:UTF-8 -*-
# 文件名:tc089_parse.py
# 创建日期:2022/3/23 16:45
# 作者:XU
# 联系邮箱:iswongx@163.com

import re

#解析 tc089.com
def tc089_par(data,dict,dict_details):

    author = re.findall('<li class="views">(.*?)</li>', data, re.S)
    if author:
        dict_details['author'] = author[0].replace('作者：', '').strip()
    else:
        dict_details['author'] = ''
    description = re.findall('<div class="single-content">.*?<p>(.*?)</p>', data, re.S)
    if description:
        dict_details['describe'] = description[0].replace('\r\n', '').replace('&nbsp;', '').strip().replace('<br/>', '').replace('&rdquo;','')
    else:
        dict_details['describe'] = ''
    dict_details['protagonist'] = ''
    tittle = re.findall(' <h1 class="entry-title">(.*?)</h1>', data, re.S)
    if tittle:
        dict_details['tittle'] = tittle[0].strip()
    else:
        dict_details['tittle'] = ''
    dict['details'] = dict_details
