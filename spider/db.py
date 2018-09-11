import os
import time
import requests
import pymongo
from neteasenews.spider.config import MONGODB_HOST, MONGODB_PORT, MONGODB_DBNAME, MONGODB_TABLE_1, MONGODB_TABLE_2, \
    MONGODB_TABLE_3


client = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
neteasenews = client[MONGODB_DBNAME]
# 集合结构:title, url, info
article = neteasenews[MONGODB_TABLE_1]
# 集合结构:title, label, comments, updatetime, keywords, url, info
mainarticle = neteasenews[MONGODB_TABLE_2]
# 集合结构:title, url, info=[desc, createdate, source, dutyeditor, imgsum, pictures]
picture = neteasenews[MONGODB_TABLE_3]
article.create_index('url')
mainarticle.create_index('url')
picture.create_index('url')


def updatedata(data, tablename):
    if data:
        if neteasenews[tablename].update({'url': data['url']}, {'$set': data}, True):
            print('=================================================\n')
            print('更新存储到数据库成功,目前{0}的文档数:{1}\t\n'.format(tablename,
                                                        neteasenews[tablename].find().count()))
            print('=================================================\n')
            print('数据展示:\n\n', data)
            return True
    else:
        print('数据不存在,无法存储到数据库,请检查是否匹配成功')


# 文章下载(纯文或者图文)
# 目前只能转化文章，若有图文无法下载图片
def write_to_sys():
    # 更新频率低
    robot = 'D:/newsdownload/article/'
    # 更新频率高
    robot_ = 'D:/newsdownload/mainarticle/'
    for item in article.find(no_cursor_timeout=True):
        try:
            if item['info']['contents']:
                path_txt = robot + str(item['title']) + '.txt'
                if not os.path.exists(robot):
                    os.makedirs(robot)
                if not os.path.exists(path_txt):
                    with open(path_txt, 'w', encoding='utf-8') as f:
                        print('{}\t数据库集合article转化为txt成功'.format(item['title']))
                        f.write(str(item['info']['contents']))
                        time.sleep(1)
        except OSError:
            pass
    print('mongodb数据库article集合转化TXT完毕')
    time.sleep(5)
    for items in mainarticle.find(no_cursor_timeout=True):
        try:
            if items['info']['contents']:
                path_txt = robot_ + str(items['title']) + '.txt'
                if not os.path.exists(robot_):
                    os.makedirs(robot_)
                if not os.path.exists(path_txt):
                    with open(path_txt, 'w', encoding='utf-8') as f:
                        print('{}\t数据库集合mainarticle转化为txt成功'.format(items['title']))
                        f.write(str(items['info']['contents']))
                        time.sleep(1)
        except OSError:
            pass


# 图集下载
def pic_to_sys():
    robot = 'D:/newsdownload/img/'
    count = 0
    # 暂时没找到取出某个键下所有值的数量的方法,先固定下载每个文档下5张图片.
    imgs = [1, 2, 3, 4, 5]
    # 从picture表找到url并且下载图片
    for item in picture.find(no_cursor_timeout=True):
        for item_imgs, img_num in zip(item['info']['pictures'], imgs):
            path = robot + str(item['title']) + '-' + str(img_num) + '.jpg'
            html = requests.get(item_imgs)
            html.raise_for_status()
            html.encoding = html.apparent_encoding
            if not os.path.exists(robot):
                os.makedirs(robot)
            if not os.path.exists(path):
                count += 1
                print('正在下载{0}张图片,标题:{1}'.format(count, item['title']))
                with open(path, 'wb') as f:
                    f.write(html.content)