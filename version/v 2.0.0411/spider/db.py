import pymongo
from neteasenews.spider.config import MONGODB_HOST, MONGODB_PORT, MONGODB_DBNAME, MONGODB_TABLE_1, MONGODB_TABLE_2, \
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

