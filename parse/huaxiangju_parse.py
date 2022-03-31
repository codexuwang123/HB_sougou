#!/usr/bin/python
# -*- coding:UTF-8 -*-
# 文件名:huaxiangju_parse.py
# 创建日期:2022/3/23 14:08
# 作者:XU
# 联系邮箱:iswongx@163.com

import re

# 解析www.huaxiangju.com
def huaxiangju_par(data, dict,dict_details):

    author = re.findall('<div class="bookPhr">.*?<dd>(.*?)</dd>', data, re.S)
    if author:
        dict_details['author'] = author[0].strip().replace('作者：')
    else:
        dict_details['author'] = ''
    description = re.findall('<div class="introCon">.*?<p><br />(.*?)</p>', data, re.S)
    if description:
        dict_details['describe'] = description[0].strip().replace('\r\n', '')
    else:
        dict_details['describe'] = ''
    dict_details['protagonist'] = ''
    tittle = re.findall('<div class="bookPhr">.*?<h2>(.*?)</h2>', data, re.S)
    if tittle:
        dict_details['tittle'] = tittle[0].strip()
    else:
        dict_details['tittle'] = ''
    dict['details'] = dict_details