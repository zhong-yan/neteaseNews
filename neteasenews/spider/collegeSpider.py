from config import *
from bs4 import BeautifulSoup
import requests
import re


# http://news.163.com/college
def html_source():
    browser = webdriver.Chrome(chrome_options=options)
    browser.get('http://news.163.com/college')
    response = requests.get('http://news.163.com/college')
    if response.status_code == 200:
        return browser.page_source


def collegespider():
    p_source = html_source()
    page = BeautifulSoup(p_source, 'lxml')
    link_1 = page.select('.himg.main_imgs > a')
    # link_2 = page.select('')
    # link_3 = page.select('')
    print(link_1)


if __name__ == "__main__":
    collegespider()
