import time
from neteasenews.spider.coldspider import datablogspider, collegespider, govspider, gongyispider, mediaspider
from neteasenews.spider.hotspider import hotspider, spider
from neteasenews.spider.rankspider import rankspider
# from neteasenews.spider.photospider import photospider
import threading
# from multiprocessing.pool import Pool


# 考虑加入downloads()方法,分类下载到本地?
# def downloads()

# 部署爬虫唯一出入口main()方法
if __name__ == '__main__':
    # 定义break条件,timeiout变量:
    timeout = 0
    print('==============================================================\n')
    print('neteasenews Spider is working now, give me some patience,ok?\n')
    print('==============================================================\n')
    print('1.爬虫全部运作\n')
    print('2.热更新(只更新即时性新闻)\n')
    print('3.冷更新(只更新变动频率低的新闻)\n')
    print('4.下载图集(需要数据库中存储有适量数据)\n')
    print('==============================================================\n')
    choices = int(input('请输入你的选择:\n\t\t\t'))
    print('--------------------------------------------------------------\n')
    if choices:
        # 如何从中断的数据开始,而不是从零开始?Redis?序列化操作?值得思考
        if choices == 1:
            while True:
                print('All of the Spider Will Be Running, Take It Easy!!!')
                try:
                    spider()
                except None:
                    pass
                time.sleep(5)
                try:
                    rankspider()
                except None:
                    pass
                time.sleep(5)
                try:
                    task_datablog = threading.Thread(target=datablogspider)
                    task_colleges = threading.Thread(target=collegespider)
                    task_gov = threading.Thread(target=govspider)
                    task_gongyi = threading.Thread(target=gongyispider)
                    task_media = threading.Thread(target=mediaspider)
                    tasks = [task_datablog, task_colleges, task_gov, task_gongyi, task_media]
                    for task in tasks:
                        task.start()
                    for task_ in tasks:
                        task_.join()
                    for task_run in tasks:
                        if task_run.is_alive():
                            print('Task is running now')
                except None:
                    pass
                time.sleep(5)
                timeout += 5
                if timeout == 10:
                    print('Spider will be off, wish no bugs or exceptions')
                    print('大吉大利,今晚吃鸡')
                    print('==============================================================\n')
                    break
        elif choices == 2:
            while True:
                try:
                    hotspider()
                except None:
                    pass
                try:
                    rankspider()
                except None:
                    pass
                # 理论上新闻更新速度根本没这么快,10S一篇新闻...666
                print('please wait for 10s,it will run again!!')
                time.sleep(10)
                timeout += 10
                # 一分钟结束,事实上并没有这么多更新快的新闻
                if timeout == 20:
                    print('热更新完毕')
                    print('大吉大利,今晚吃鸡')
                    print('==============================================================\n')
                    break
        elif choices == 3:
            while True:
                try:
                    task_datablog = threading.Thread(target=datablogspider)
                    task_colleges = threading.Thread(target=collegespider)
                    task_gov = threading.Thread(target=govspider)
                    task_gongyi = threading.Thread(target=gongyispider)
                    task_media = threading.Thread(target=mediaspider)
                    tasks = [task_datablog, task_colleges, task_gov, task_gongyi, task_media]
                    for task in tasks:
                        task.start()
                    for task_ in tasks:
                        task_.join()
                    for task_run in tasks:
                        if task_run.is_alive():
                            print('Task is running now')
                except None:
                    pass
                time.sleep(5)
                timeout += 5
                if timeout == 10:
                    print('冷更新完毕')
                    print('大吉大利,今晚吃鸡')
                    print('==============================================================\n')
                    break
        elif choices == 4:
            print('暂时未做处理!因为chromedriver速度太慢了')
    time.sleep(10)
    print('==============================================================\n')
    print('Spider will be off, wish no bugs or exceptions')
    print('\t\t\t大吉大利\t\t今晚吃鸡')
    print('==============================================================\n')
    # 展示部分数据



