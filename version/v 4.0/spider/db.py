import os

import pymongo
import requests

from config import MONGODB_HOST, MONGODB_PORT, MONGODB_DBNAME, MONGODB_TABLE_1, MONGODB_TABLE_2, \
    MONGODB_TABLE_3

client = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
neteasenews = client[MONGODB_DBNAME]
article = neteasenews[MONGODB_TABLE_1]
coldpage = neteasenews[MONGODB_TABLE_2]
picture = neteasenews[MONGODB_TABLE_3]
article.create_index('url')
coldpage.create_index('url')
picture.create_index('url')


def updatedata(data, tablename):
    if data:
        if neteasenews[tablename].update({'url': data['url']}, {'$set': data}, True):
            print('=======================================================================================\n')
            print('更新存储到数据库成功,目前{0}的文档数:{1}\t\n'.format(tablename,
                                                        neteasenews[tablename].find().count()))
            print('=======================================================================================\n')
            print('数据展示:\n\n', data)
            return True
    else:
        print('数据不存在,无法存储到数据库,请检查是否匹配成功')


def db_img():
    # 从数据库中取出带有图片信息的文章信息存储到pictures里面
    for item in article.find():
        if item['info']:
            data_img = {
                'title': item['title'],
                'url': item['url'],
                'info': [p['pictures'] for p in item['info']]
            }
            updatedata(data_img, MONGODB_TABLE_3)


# 文字加图片形式
def write_to_sys():
    robot = 'D:/newsdownload/'
    count = 0
    for item in article.find():
        try:
            # 文字
            if item['info']['contents']:
                with open(r'D:\\neteasenews download\\article\{}'.format(
                        item['title'] + '.txt'), 'w', encoding='utf-8') as f:
                        f.write(str(item['info']['contents']))
            # 图片
            for item_img in item['info']['pictures']:
                path = robot + str(item['title']) + '.jpg'
                html = requests.get(item_img)
                html.raise_for_status()
                html.encoding = html.apparent_encoding
                if not os.path.exists(robot):
                    os.makedirs(robot)
                if not os.path.exists(path):
                    count += 1
                    print('正在下载{0}张图片,标题:{1}'.format(count, item['title']))
                    with open(path, 'wb') as f:
                        f.write(html.content)
        except OSError:
            pass
    for item_ in coldpage.find():
        try:
            if item_['contents']:
                with open(r'D:\\neteasenews download\\coldpage\{}'.format(
                        item_['title'] + '.txt'), 'w', encoding='utf-8') as f:
                        f.write(str(item_['contents']))
        except OSError:
            pass


def pic_to_sys():
    robot = 'D:/newsdownload/'
    count = 0
    # 从picture表找到url并且下载图片
    for item in picture.find():
        for item_img in item['info']['pictures']:
            path = robot + str(item['title']) + '.jpg'
            html = requests.get(item_img)
            html.raise_for_status()
            html.encoding = html.apparent_encoding
            if not os.path.exists(robot):
                os.makedirs(robot)
            if not os.path.exists(path):
                count += 1
                print('正在下载{0}张图片,标题:{1}'.format(count, item['title']))
                with open(path, 'wb') as f:
                    f.write(html.content)