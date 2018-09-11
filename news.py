import time
from neteasenews.spider.spider import rankspider, datablogspider, collegespider, govspider, \
    gongyispider, mediaspider
from neteasenews.spider.mainspider import mainspider, photospider
from neteasenews.spider.db import write_to_sys, pic_to_sys
import threading


# 部署爬虫唯一出入口main()方法
if __name__ == '__main__':
    print('===========================\n')
    print('neteasenews Spider is working now, give me some patience,ok?\n')
    print('===========================\n')
    print('1:爬虫全部运作\n')
    print('2:采集即时性新闻\n')
    print('3:采集变动频率低的新闻)\n')
    print('4:数据库处理(文本和图片本地化)\n')
    print('===========================\n')
    choices = int(input('请输入你的选择:\n\t\t\t'))
    print('----------------------------\n')
    if choices:
        if choices == 1:
            print('All of the Spider Will Be Running, Take It Easy!!!')
            mainspider()
            photospider()
            rankspider()
            # 获取数读,新闻学院,政务,公益,媒体导航标签里面的内容,开启多线程.
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
                    print('Task:{} is running now'.format(task_run))
            time.sleep(5)
            print('Spider will be off, wish no bugs or exceptions')
            print('The choice 1 :sucess to crawl ')
            print('=========================\n')
        elif choices == 2:
            timeout_news = 0
            while True:
                mainspider()
                # 理论上新闻更新速度根本没这么快.10S一篇最新新闻?
                print('please wait for 10s,it will run again!!')
                time.sleep(5)
                timeout_news += 5
                # 只爬取10分钟
                if timeout_news == 10:
                    print('==========================\n')
                    print('The choice 2 :sucess to crawl ')
                    print('==========================\n')
                    break
        elif choices == 3:
            rankspider()
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
            time.sleep(10)
            photospider()
            print('============================\n')
            print('The choice 3 :sucess to crawl ')
            print('============================\n')
        elif choices == 4:
            write_to_sys()
            pic_to_sys()
            print('=============================\n')
            print('The choice 4 :sucess to crawl ')
            print('=============================\n')
    time.sleep(10)
    print('================================\n')
    print('Spider will be off, wish no bugs or exceptions')
    print('\t\t\tsucess to crawl')
    print('================================\n')
