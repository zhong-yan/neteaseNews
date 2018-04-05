from spider.config import *

timeout = 1
for i in shehui.distinct('articleUrl'):
    timeout += 1
    print('第{0}文章URL:{1}'.format(timeout, i))
