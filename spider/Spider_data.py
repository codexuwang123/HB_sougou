#!/usr/bin/python
# -*- coding:UTF-8 -*-
# 文件名:Spider_data.py
# 创建日期:2022/3/10 10:23
# 作者:XU
# 联系邮箱:iswongx@163.com
import time

import requests
import re
from parse import format_base_spdb
from settings import set_log
import random
from to_sql import save_data_to_sql
from redis_client import redis_connect
import json
from settings import set_

conn = redis_connect.Redis_connect()
s_data = save_data_to_sql.Save_score_to_sql()
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
    def spider_sougou(self, page, list_redis, keyword=None, ):

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

            format_base_spdb.format_text(first_data_list=data, tittle_list=tittle, keyword=keyword, ssin=None,
                                         list_redis=list_redis)
        else:
            print(res.text)


# 主函数调用
def last_mains():
    # 数据库获取关键次列表
    keyword_list = s_data.get_keyword()
    if keyword_list:
        for i in keyword_list:
            list_redis = []
            dict_redis = {}
            dict_redis['book_name'] = i.get('Search_Keyword')
            print(dict_redis)
            for n in range(1, set_.get('max_page')):
                spider_self = Spider_desc_sougou(wd=i.get('Search_Keyword'))
                spider_self.spider_sougou(page=n, keyword=spider_self.wd, list_redis=list_redis)
            dict_redis['data'] = list_redis
            dict_ = json.dumps(dict_redis, ensure_ascii=False)
            print(dict_)
            conn.insert_data_redis(redis_key='sougou', values=dict_)
            # 更新爬虫状态
            s_data.undate_data(status_='1', keyword=i.get('Search_Keyword'))
            print('redis 数据存放成功')

    else:
        print('========温馨提示：没有有效关键词需要爬取=======')


if __name__ == "__main__":
    while True:
        time.sleep(3)
        last_mains()
