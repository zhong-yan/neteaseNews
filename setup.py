#! ./Administrator/AppData/Local/Programs/Python/Python37-32
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import spider

setup(
        name="Taohuazu",
        version="5.0",
        keywords=("news"),
        description="news' script",
        long_description="A crawler script that collects website news",
        license="Apache License 2.0",

        url="https://github.com/zhong-yan/Taohuazu",
        author="zhongyan",
        author_email="zhongygg@gmail.com",

        packages=find_packages(include=spider),
        include_package_data=True,
        platforms="any",
        install_requires=[
            'bs4>=0.0.1',
            'requests>=2.19.1',
            'beautifulsoup4>=4.6.3',
            'lxml>=4.2.4',
            'urllib3>=1.23',
            'selenium>=3.14.0',
            'pymongo>=3.7.1'
        ],
        zip_safe=False
)