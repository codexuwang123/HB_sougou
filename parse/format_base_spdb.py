#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名: format_base_spdb.py
# 作者:WangXu
# 联系邮箱:iswongx@163.com

# 格式化基本信息
import random
import re
import uuid
import requests
import xmla_parse
import parse_baidu
import ysg_parse
import qbxsw_parse
import aixswx_parse
import mq_parse
import rx_parse
import qt_parse
import soxs_parse
import zjsw_org_parse
import iqixs_parse
import biqusz_parse
import haipu_xs_parse
import soxscc_parse
import xuanshu_parse
import uuxshuo_parse
import luochen_parse
import m_bxwxorg_parse
import shuchu_parse
import time
import tc089_parse
import xsorg18_parse
import rpg66_parse
import wenxue_iqiy
import sxcnw_parse
import yjgmmc_par
import xsb_xs_parse
import xxshuyuan_parse
import jipinxx_parse
from to_sql import save_data_to_sql
import phone_sxcnw
import hongshu_parse
import huaxiangju_parse
import baihexs_parse
import shouda88_parse
import ujwang_parse
from settings import ua
import laishu8
import qmzhongwen_parse
from settings import set_log
from redis_client import redis_connect
import json
import urllib3
from spider import Spider_data
from settings import ua

urllib3.disable_warnings()
logging_ = set_log()
conn = redis_connect.Redis_connect()


# 获取真实页面方法
def get_true(url, ssin=None):
    string = re.findall(r'https{0,1}://(.*?)\/', url)
    if string:
        uA = ua.get('user_agent')
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate',
            'If-None-Natch': '',
            'If-Modified-Since': '',
            'user-agent': random.choice(ua.get('user_agent')),
        }
        print('=============================当前正在进入：{} ===================================='.format(url))
        try:
            res = requests.get(url, headers=headers, timeout=20, verify=False)
            time.sleep(0.5)
            if res.status_code == 200:
                info = res.text
                char = re.findall('charset="{0,1}(.*?)"', info, re.S)
                if char:
                    try:
                        info1 = res.content.decode(encoding='{}'.format(char[0].lower()))
                        return info1, res.url
                    except Exception as e:
                        print(e, '异常编码了================')
                        return info, res.url
                else:
                    logging_.info('编码异常-连接为{}，'.format(res.url))
                    return '编码异常', res.url
            else:
                print('状态码异常返回数据', res.text)
                logging_.info('状态码/服务异常-被访问链接为{}，'.format(res.url))
                return '服务异常', res.url
        except Exception as e:
            print(e, '异常')
            headers1 = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Accept-Encoding': 'gzip, deflate',
                'If-None-Natch': '',
                'If-Modified-Since': '',
                'Host': string[0],
                'user-agent': random.choice(ua.get('user_agent'))
            }
            print('进入重定向了======1111 主意呀=========')
            try:
                res = requests.get(url, headers=headers1, timeout=20, verify=False)
                logging_.info('特殊异常{}，异常连接{}'.format(e, url))
                return res.text, url
            except Exception as e:
                print(e, '---------')
                return '超时', url


# 详情页解析
def format_data(data, dict):
    dict_details = {}
    author = ''
    # 作者名称
    author2 = re.findall('<meta property="og:novel:author" content="(.*?)"', data)
    if author2:
        author = author2[0]
        dict_details['author'] = author
    else:
        dict_details['author'] = author

    # 主角(默认为空)
    protagonist = ''
    if '主角' in data:
        protagonist = re.findall('主角：(.*?)<', data)
        if protagonist:
            dict_details['protagonist'] = protagonist[0]
        else:
            dict_details['protagonist'] = ''
    else:
        dict_details['protagonist'] = protagonist
    # 小说简介
    describe = re.findall('<meta property="og:description" content="(.*?)"', data, re.S)
    if describe:
        string = re.sub('&#\d+;', '', describe[0])
        dict_details['describe'] = string.replace('<br />\n', '').replace('<br />', '').replace('&ldquo;', '').replace(
            '&rdquo;', '').replace('&nbsp;', '').replace('&hellip;', '').replace('\n', '').replace('<br/>', '').replace(
            '\\u3000', '').replace('\t\t','')
    else:
        dict_details['describe'] = ''

    # 章节标题
    tittle = ''
    # 默认为空
    dict_details['tittle'] = tittle
    dict['details'] = dict_details


# 首页数据解析
def format_text(first_data_list, tittle_list, keyword, ssin=None):
    list = []
    for i, n in zip(first_data_list, tittle_list):
        number = str(uuid.uuid1()).replace('-', '')
        dict = {}
        if 'http:' in i:
            i = i
        else:
            i = 'https://www.sogou.com' + i

        n = n.replace('</em>', '').replace('red', '').replace('beg', '').replace('<em>', '').replace('end', '').replace(
            '<!--_-->', '').replace('\r\n', '').strip()

        # 更进一步解析获取的脏数据
        new_url = i
        dict['number'] = number
        dict['tittle'] = n
        # 跳转链接
        dict['url'] = new_url
        # 真实链接
        dict['true_url'] = ''
        dict['keyword'] = keyword
        dict_ = json.dumps(dict)
        print(dict_, '===========')
        conn.insert_data_redis(redis_key='sougou', values=dict_)


# 搜狗获取真是链接程序
def get_sougou_rue_url(skip_url):
    string = re.findall('https{0,1}://(.*?)\/', skip_url)
    if string:
        headers = {
            'Connection': 'keep-alive',
            'User-Agent': random.choice(ua.get('user_agent'))
        }
        try:
            res = requests.get(skip_url, headers=headers, verify=False)
            if res.status_code == 200:
                info = res.text
                data1 = re.findall("URL='(.*?)'", info)
                print(data1, '真实链接==1kokofklsflsk')
                if data1:
                    return data1[0]
                else:
                    # print(res.text, '获取真实链接异常 text 0000000000000222222222222222222222222')
                    print(skip_url, '获取真实链接异常 url 0000000000000222222222222222222222222')
                    return skip_url
        except Exception as e:
            print(e, '真实连接')
            res = requests.get(skip_url, headers=headers, verify=False)
            if res.status_code == 200:
                info = res.text
                data1 = re.findall("URL='(.*?)'", info)
                if data1:
                    return data1[0]
            return skip_url


# 主要解析程序
def get_():
    print('线程进来了================')
    dta = conn.search_data_redis(redis_key='sougou')
    if dta:
        dict = json.loads(dta)
        new_tittle = dict.get('tittle')
        new_url = dict.get('url')
        print(type(new_url), new_url, '000000011111111111111111111111111')
        true_url1 = get_sougou_rue_url(skip_url=new_url)
        details_data, true_url = get_true(url=true_url1)
        dict['true_url'] = true_url
        new_keyword = dict.get('keyword')
        if new_keyword in new_tittle:
            if details_data == '编码异常':
                print('编码异常====', true_url)
                return None
            if details_data == '超时':
                print('超时了------------------', true_url)
                return None
            if details_data == '服务异常':
                print('服务异常=================', true_url)
                return None
            if 'ximalaya' in true_url:
                xmla_parse.smly_(data=details_data, dict=dict)
            elif 'https://dushu.baidu.com/' in true_url:
                print('进入百度链接了')
                parse_baidu.parse_b(url=true_url, dict=dict)
            elif 'luochen' in true_url:
                luochen_parse.parse_ysg(data=details_data, dict=dict)
                print('落尘图书')
            elif '来书吧' in details_data:
                laishu8.lais(data=details_data, dict=dict)
            elif '阅书阁' in details_data:
                ysg_parse.parse_ysg(data=details_data, dict=dict)
            elif '全本小说网' in new_tittle:
                qbxsw_parse.qbxsw_parse(data=details_data, dict=dict)
            elif '蜻蜓FM' in new_tittle:
                qt_parse.qt_par(data=details_data, dict=dict)
            elif '<p id="summary">' in details_data:
                mq_parse.mq_par(data=details_data, dict=dict)
            elif '若夏' in new_tittle:
                rx_parse.rx_par(data=details_data, dict=dict)
            elif '七猫中文网' in new_tittle:
                for i in range(5):
                    time.sleep(1)
                    data2 = qmzhongwen_parse.get_acw_sc_v2(base_url=true_url)
                    if '七猫中文网' in data2:
                        qmzhongwen_parse.qimao_parse(data=data2, dict=dict)
                        break
                    else:
                        print('七猫没进去========')
                        continue
            elif 'www.soxs.cc' in true_url:
                soxs_parse.soxs_par(data=details_data, dict=dict)
            elif 'www.xuanshu.com' in true_url:
                xuanshu_parse.quanshu(data=details_data, dict=dict)
            elif 'www.uuxsw' in true_url:
                uuxshuo_parse.uuxs_par(data=details_data, dict=dict)
            elif 'quanben' in true_url:
                qbxsw_parse.qbxsw_parse(data=details_data, dict=dict)
            elif 'shuchu' in true_url:
                shuchu_parse.shuchu_par(data=details_data, dict=dict)
                print('书橱进来了====')
            elif '66rpg.com' in true_url:
                rpg66_parse.chenguang_par(data=details_data, dict=dict)
            elif 'wenxue.iqiyi' in true_url:
                wenxue_iqiy.iqiy(data=details_data, dict=dict)
            elif 'http://www.sxcnw' in true_url:
                sxcnw_parse.sxdz_par(data=details_data, dict=dict)
            elif 'www.xxsy.net' in true_url:
                xxshuyuan_parse.xxshuyuan_par(data=details_data, dict=dict)
            elif 'm.sxcnw.net' in true_url:
                phone_sxcnw.phone_sxcnw(data=details_data, dict=dict)
            elif 'www.yjgmmc' in true_url:
                yjgmmc_par.eryuet_par(data=details_data, dict=dict)
            elif 'www.soxscc.org' in true_url:
                soxscc_parse.soxscc_par(data=details_data, dict=dict)
            elif 'www.hongshu.com' in true_url:
                hongshu_parse.hongshu_par(data=details_data, dict=dict)
            elif 'www.xsb-xs.com' in true_url:
                xsb_xs_parse.xsb_xs_par(data=details_data, dict=dict)
            elif 'www.jipinxx.com' in true_url:
                jipinxx_parse.jipinxx_par(data=details_data, dict=dict)
            elif 'www.huaxiangju.com' in true_url:
                huaxiangju_parse.huaxiangju_par(data=details_data, dict=dict)
            elif 'www.baihexs.com' in true_url:
                baihexs_parse.baihexs_par(data=details_data, dict=dict)
            elif 'm.bxwxorg.com' in true_url:
                m_bxwxorg_parse.m_bxwxorg_par(data=details_data, dict=dict)
            elif 'www.shouda88.com' in true_url:
                shouda88_parse.shouda88_par(data=details_data, dict=dict)
            elif 'm.rmxsba.com' in true_url:
                m_bxwxorg_parse.m_bxwxorg_par(data=details_data, dict=dict)
            elif 'www.18xsorg.com' in true_url:
                xsorg18_parse.xsorg18_par(data=details_data, dict=dict)
            elif 'www.haipu-xs.com' in true_url:
                haipu_xs_parse.haipu_xs_par(data=details_data, dict=dict)
            elif 'www.biqusz.com' in true_url:
                biqusz_parse.biqusz_par(data=details_data, dict=dict)
            elif 'www.zjsw.org' in true_url:
                zjsw_org_parse.zjsw_org_psr(data=details_data, dict=dict)
            elif 'www.tc089.com' in true_url:
                tc089_parse.tc089_par(data=details_data, dict=dict)
            elif 'www.iqixs.com' in true_url:
                iqixs_parse.iqixs_par(data=details_data, dict=dict)
            elif 'www.ujwang.com' in true_url:
                ujwang_parse.ujwang_par(data=details_data, dict=dict)
            elif 'www.aixswx.com' in true_url:
                aixswx_parse.aixswx_par(data=details_data, dict=dict)
            else:
                format_data(data=details_data, dict=dict)

            # 数据库存放数据
            sql_server = save_data_to_sql.Save_score_to_sql()
            sql_server.search_data_to_sql(data=dict)
            sql_server.details_data_to_sql(data=dict)
            # list.append(dict)
            # print(dict)
            return new_keyword
        else:
            print('不符合跳过0000000000000000000000000000000000')
            print(new_tittle, '111111111111111111')
            print(true_url, '2222222222222222')
    else:
        print('数据爬取完成====')


if __name__ == '__main__':

    # s = Spider_data.Spider_desc_sougou(wd='一品毒妃')
    # s.spider_sougou(page='5', keyword=s.wd)
    try:
        while True:
            get_()
            time.sleep(3)
    except KeyboardInterrupt as e:
        print(e, '强制中断 异常捕获===')


with pd.ExcelWriter(r'C:\Users\数据\Desktop\data\test2.xls') as writer:
    df1.to_excel(writer, sheet_name='df1')
    df2.to_excel(writer, sheet_name='df2')