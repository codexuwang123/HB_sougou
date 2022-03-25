#!/usr/bin/python
# -*- coding:UTF-8 -*-
# 文件名:Spider_data.py
# 创建日期:2022/3/10 10:23
# 作者:XU
# 联系邮箱:iswongx@163.com

import requests
import re
from parse import format_base_spdb
from settings import set_log
import random

list = []
logging_ = set_log()

from settings import ua


# 主要爬虫方法
class Spider_desc_sougou():

    # 基本请求头配置
    def __init__(self, wd):
        self.uA = ua.get('user_agent')
        self.wd = wd
        logging_.info('搜索引擎搜狗，正在爬取={}相关内容。'.format(self.wd))

    # 解析主函数
    def spider_sougou(self, page, keyword=None):
        # '&_ast=&&&&&&&&lkt=0%2C0%2C0&&&oq=&ri=0&sourceid=sugg&&stj=0%3B6%3B0%3B0&stj2=0&stj0=0&stj1=6&hp=36&hp1=&suglabid=suglabId_1'
        self.url = 'https://www.sogou.com/web?'
        self.params = {
            'query': keyword,
            '_asf': 'www.sogou.com',
            'w': '01015002',
            'p': '40040108',
            'ie': 'utf8',
            's_from': 'index',
            'sut': '229091',
            'from': 'index-nologin',
            'sst0': '1647942925355',
            'sugsuv': '1646894831150286',
            'sugtime': '1647942925355',
            'suguuid': '8b531100-b520-4d21-8d9f-074d40f77c4f',
            'page': page,
            'src': 'srp_paging',
            'fr': 'none'
        }
        self.headers = {
            'User-Agent': random.choice(self.uA),
            'X-Requested-With': 'XMLHttpRequest'
        }
        res = requests.get(self.url, headers=self.headers, params=self.params, verify=False)
        if res.status_code == 200:
            data = re.findall('<h3.*?class="vr-title.*?".*?href="(.*?)"', res.text, re.S)
            tittle = re.findall('<h3.*?class="vr-title.*?".*?<em>(.*?)</a>', res.text, re.S)

            format_base_spdb.format_text(first_data_list=data, tittle_list=tittle, keyword=keyword, ssin=None)
        else:
            print(res.text)
