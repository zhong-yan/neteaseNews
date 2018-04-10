import json
import requests
from requests.exceptions import RequestException
from neteasenews.spider.config import JSON_INDEX_URLS
from neteasenews.spider.contents import info_news, info_datalog, info_photoview
from multiprocessing.pool import Pool


# 爬取要闻,广州,社会,国内,国际,独家,军事,财经,科技,体育,娱乐,时尚,汽车,房产,航空,健康
def parse(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # 解析json,运用replace()使得该字符串符合json语法,否则会出现编码解码异常,即无法loads()
            response_json = json.loads(response.text.replace('data_callback(', '').replace(')', ''))
            for item in response_json:
                data_news = info_news(item.get('docurl'))
                data_datablog = info_datalog(item.get('docurl'))
                data_phtoview = info_photoview(item.get('docurl'))
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
                    print(infomation_news)
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
                    print(infomation_datalog)
                elif data_phtoview:
                    pass
                    # infomation_photoview = {
                    #     'type': item.get('channelname'),
                    #     'title': item.get('title'),
                    #     'comments': item.get('tienum'),
                    #     'updatetime': item.get('time'),
                    #     'keywords': [key.get('keyname') for key in item.get('keywords')],
                    #     'url': item.get('docurl'),
                    #     'info': data_phtoview
                    # }
                    # print(infomation_photoview)
    except RequestException:
        pass
    except ConnectionError:
        print('连接失败,请重试!')
        pass


def get_next_urls():
    links = []
    base_url = 'http://temp.163.com/special/00804KVA/'
    for k in range(2, 11):
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
        links.append(url_yaomen)
        links.append(url_guangzhou)
        links.append(url_shehui)
        links.append(url_guonei)
        links.append(url_dujia)
        links.append(url_war)
        links.append(url_money)
        links.append(url_tech)
        links.append(url_sports)
        links.append(url_ent)
        links.append(url_lady)
        links.append(url_auto)
        links.append(url_houseguangzhou)
        links.append(url_hangkong)
        links.append(url_jiankang)
    return links


if __name__ == '__main__':
    url_ = []
    for i in JSON_INDEX_URLS:
        url_.append(i)
    url_data = get_next_urls()
    urls = url_ + url_data
    pool = Pool(10)
    pool.map(parse, urls)

