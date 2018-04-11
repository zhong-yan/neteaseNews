import json
import requests
from requests.exceptions import RequestException
from neteasenews.spider.config import JSON_INDEX_URLS
from neteasenews.spider.contents import info_news, info_datalog, info_photoview, info_dy
from multiprocessing.pool import Pool
from neteasenews.spider.db import updatedata, MONGODB_TABLE_1


# 爬取要闻,广州,社会,国内,国际,独家,军事,财经,科技,体育,娱乐,时尚,汽车,房产,航空,健康,无人机
def parse(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # 解析json,运用replace()使得该字符串符合json语法,否则会出现编码解码异常,即无法loads()
            response_json = json.loads(response.text.replace('data_callback(', '').replace(')', ''))
            for item in response_json:
                # 网易正文
                data_news = info_news(item.get('docurl'))
                # 数读平台
                data_datablog = info_datalog(item.get('docurl'))
                # 图集
                # data_phtoview = info_photoview(item.get('docurl'))
                # 网易号:
                data_dy = info_dy(item.get('docurl'))
                if data_news:
                    infomation_news = {
                        'type': item.get('channelname'),
                        'title': item.get('title'),
                        'comments': item.get('tienum'),
                        'updatetime': item.get('time'),
                        'keywords': [key.get('keyname') for key in item.get('keywords')],
                        'url': item.get('docurl'),
                        'info': data_news
                    }
                    updatedata(infomation_news, MONGODB_TABLE_1)
                elif data_datablog:
                    infomation_datalog = {
                        'type': item.get('channelname'),
                        'title': item.get('title'),
                        'comments': item.get('tienum'),
                        'updatetime': item.get('time'),
                        'keywords': [key.get('keyname') for key in item.get('keywords')],
                        'url': item.get('docurl'),
                        'info': data_datablog
                    }
                    updatedata(infomation_datalog, MONGODB_TABLE_1)
                # elif data_phtoview:
                #     pass
                #     infomation_photoview = {
                #         'type': item.get('channelname'),
                #         'title': item.get('title'),
                #         'comments': item.get('tienum'),
                #         'updatetime': item.get('time'),
                #         'keywords': [key.get('keyname') for key in item.get('keywords')],
                #         'url': item.get('docurl'),
                #         'info': data_phtoview
                #     }
                #     updatedata(infomation_photoview, MONGODB_TABLE_1)
                elif data_dy:
                    infomation_dy = {
                        'type': item.get('channelname'),
                        'title': item.get('title'),
                        'comments': item.get('tienum'),
                        'updatetime': item.get('time'),
                        'keywords': [key.get('keyname') for key in item.get('keywords')],
                        'url': item.get('docurl'),
                        'info': data_dy
                    }
                    updatedata(infomation_dy, MONGODB_TABLE_1)
    except RequestException:
        pass
    except ConnectionError:
        print('连接失败,请重试!')
        pass


def get_next_urls():
    link = []
    base_url = 'http://temp.163.com/special/00804KVA/'
    for k in range(2, 11):
        # 首页---start
        url_yaomen = base_url + 'cm_yaowen_0{}.js?callback=data_callback'.format(k)
        url_guangzhou =\
            'http://house.163.com/special/00078GU7/guangzhou_xw_news_v1_0{}.js?callback=data_callback'.format(k)
        url_shehui = base_url + 'cm_shehui_0{}.js'.format(k)
        url_guonei = base_url + 'cm_guonei_0{}.js'.format(k)
        url_dujia = base_url + 'cm_dujia_0{}.js'.format(k)
        url_war = base_url + 'cm_war_0{}.js'.format(k)
        url_money = base_url + 'cm_money_0{}.js'.format(k)
        url_tech = base_url + 'cm_tech_0{}.js'.format(k)
        url_sports = base_url + 'cm_sports_0{}.js'.format(k)
        url_ent = base_url + 'cm_ent_0{}.js'.format(k)
        url_lady = base_url + 'cm_lady_0{}.js'.format(k)
        url_auto = base_url + 'cm_auto_0{}.js'.format(k)
        url_houseguangzhou = base_url + 'cm_houseguangzhou_0{}.js'.format(k)
        url_hangkong = base_url + 'cm_hangkong_0{}.js'.format(k)
        url_jiankang = base_url + 'cm_jiankang_0{}.js'.format(k)
        # 首页---END
        # 无人机--start
        url_uav = 'http://news.163.com/uav/special/000189N0/uav_index_0{}.js?callback=data_callback'.format(k)
        # 无人机---END
        link.append(url_yaomen)
        link.append(url_guangzhou)
        link.append(url_shehui)
        link.append(url_guonei)
        link.append(url_dujia)
        link.append(url_war)
        link.append(url_money)
        link.append(url_tech)
        link.append(url_sports)
        link.append(url_ent)
        link.append(url_lady)
        link.append(url_auto)
        link.append(url_houseguangzhou)
        link.append(url_hangkong)
        link.append(url_jiankang)
        link.append(url_uav)
    links = link + JSON_INDEX_URLS
    return links


def hotspider():
    pool = Pool(5)
    pool.map(parse, JSON_INDEX_URLS)


def spider():
    url_data = get_next_urls()
    pool = Pool(5)
    pool.map(parse, url_data)
    # pool.join()
