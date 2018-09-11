import pymongo
from .config import MONGODB_HOST, MONGODB_PORT, MONGODB_DBNAME, MONGODB_TABLE_1, MONGODB_TABLE_2, \
    MONGODB_TABLE_3, MONGODB_TABLE_4

client = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
neteasenews = client[MONGODB_DBNAME]
article = neteasenews[MONGODB_TABLE_1]
newsrank = neteasenews[MONGODB_TABLE_2]
coldpage = neteasenews[MONGODB_TABLE_3]
picture = neteasenews[MONGODB_TABLE_4]
article.create_index('url')
newsrank.create_index('url')
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


def db_img_url():
    pictures = []
    for item in article.find():
        if item['info']:
            pictures.append(p['pictures'] for p in item['info'])
    for i in newsrank.find():
        if i['pictures']:
            pictures.append(i['pictures'])
    return pictures


def write_to_sys():
    for item in article.find():
        try:
            if item['info']['contents']:
                with open(r'D:\\neteasenews download\\article\{}.txt'.format(item['title']), 'w', encoding='utf-8') as f:
                        f.write(str(item['info']['contents']))
        except OSError:
            pass
    for item_ in coldpage.find():
        try:
            if item_['contents']:
                with open(r'D:\\neteasenews download\\coldpage\{}.txt'.format(item_['title']), 'w', encoding='utf-8') as f:
                        f.write(str(item_['contents']))
        except OSError:
            pass
    for item_l in newsrank.find():
        try:
            if item_l['contents']:
                with open(r'D:\\neteasenews download\\coldpage\{}.txt'.format(item_l['title']), 'w', encoding='utf-8') as f:
                        f.write(str(item_l['contents']))
        except OSError:
            pass
