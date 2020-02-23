# _*_coding:utf8_*_
# Project: lin_mass_tools
# File: visitor.py
# Author: ClassmateLin
# Email: 406728295@qq.com
# Time: 2020/2/23 7:54 上午
# DESC:
import abc
import requests
import re
import random
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Visitor(metaclass=abc.ABCMeta):
    """
    访问者抽象类
    """

    def visit(self, url, proxy):
        """
        访问URL
        :param url:
        :param proxy:代理
        :return:
        """
        pass


class RequestVisitor(Visitor):
    """
    访问者具体实现类
    """

    def __init__(self):
        self._headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
        }

    def _refresh_headers(self):
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
            'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116'
            ' Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 '
            'Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/32.0.1667.0 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
            'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko)'
            ' Chrome/27.0.1453.116 Safari/537.36']
        user_agent = random.choice(user_agent_list)
        self._headers['User-Agent'] = user_agent

    def visit(self, url, proxy):
        """
        访问链接
        :param url:
        :param proxy:
        :return:
        """
        self._refresh_headers()
        try:
            resp = requests.get(url, headers=self._headers, proxies=proxy, verify=False, allow_redirects=False,
                                timeout=5)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                read_num_text = soup.find('span', {'class': 'read-count'}).text
                read_num = re.findall(r"\d+", read_num_text)[0]
                return int(read_num)
            return 0

        except Exception as e:
            print(e.args)
            return 0


if __name__ == '__main__':
    visitor = RequestVisitor()
    res = visitor.visit(url='https://blog.csdn.net/ClassmateLin/article/details/104441828', proxy={
        'http': 'http://185.220.101.10:3128'
    })
    print(res)
