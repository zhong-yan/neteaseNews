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
    print('5:网页文本自动化采集系统测试')
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
        elif choices == 5:
            print('\t\t\t1:采集富有js渲染的标签页,例如首页,存储到集合mainarticle\n')
            print('\t\t\t2:采集"图片"标签以及存在别处的图片新闻链接,存储到集合picture\n')
            print('\t\t\t3:采集"排行"标签,存储到集合article\n')
            print('\t\t\t4:采集"数读"标签,存储到集合article\n')
            print('\t\t\t5:采集"新闻学院"标签,存储到集合article\n')
            print('\t\t\t6:采集"政务"标签,存储到集合article\n')
            print('\t\t\t7:采集"公益"标签,存储到集合article\n')
            print('\t\t\t8:采集"媒体"标签,存储到集合article\n')
            print('\t\t\t9:正文等内容保存到本地(D:/newsdownload/article/)\n')
            print('\t\t\t10:下载图片到本地(D:/newsdownload/img/)\n')
            TEST = input('请输入你要测试的是哪个选项:\n')
            if TEST == 1:
                mainspider()
            elif TEST == 2:
                photospider()
            elif TEST == 3:
                rankspider()
            elif TEST == 4:
                datablogspider()
            elif TEST == 5:
                collegespider()
            elif TEST == 6:
                govspider()
            elif TEST == 7:
                gongyispider()
            elif TEST == 8:
                mediaspider()
            elif TEST == 9:
                write_to_sys()
            elif TEST == 10:
                pic_to_sys()

    time.sleep(10)
    print('================================\n')
    print('Spider will be off, wish no bugs or exceptions')
    print('\t\t\tsucess to crawl')
    print('================================\n')
