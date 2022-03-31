#!/usr/bin/python
# -*- coding:UTF-8 -*-
# 文件名:zjsw_org_parse.py
# 创建日期:2022/3/23 16:39
# 作者:XU
# 联系邮箱:iswongx@163.com

import re

#解析 www.zjsw.org
def zjsw_org_psr(data,dict,dict_details):

    author = re.findall('<div class="bookname">.*?<em>(.*?)</em>', data, re.S)
    if author:
        dict_details['author'] = author[0].replace('作者：', '').strip()
    else:
        dict_details['author'] = ''
    description = re.findall('<div class="intro">(.*?)</div>', data, re.S)
    if description:
        dict_details['describe'] = description[0].replace('\r\n', '').replace('&nbsp;', '').strip().replace('<br/>', '')
    else:
        dict_details['describe'] = ''
    dict_details['protagonist'] = ''
    tittle = re.findall('<div class="bookname">.*?<h1 class="f20h">(.*?)<em>', data, re.S)
    if tittle:
        dict_details['tittle'] = tittle[0].strip()
    else:
        dict_details['tittle'] = ''
    dict['details'] = dict_details
