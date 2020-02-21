# _*_coding:utf8_*_
# Project: increment_visitor
# File: main.py
# Author: ClassmateLin
# Email: 406728295@qq.com
# Time: 2020/2/13 8:05 下午
# DESC:
import configparser
import abc
import random
import time
import requests
import hashlib
import urllib3
from bs4 import BeautifulSoup
from threading import Thread

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Visitor(metaclass=abc.ABCMeta):
    """
    访问者抽象类
    """
    @abc.abstractmethod
    def visit(self, url):
        pass


class RequestVisitor(Visitor):
    """
    访问者具体实现类
    """
    def __init__(self, order_no='', secret=''):
        self._order_no = order_no  # 讯代理 动态代理订单号
        self._secret = secret  # 讯代理秘钥
        self._proxy, auth = self._init_proxy()
        self._headers = self._init_headers(auth)

    def _init_proxy(self):
        """
        使用讯代理
        :return:
        """
        ip = "forward.xdaili.cn"
        port = "80"
        ip_port = ip + ":" + port
        timestamp = str(int(time.time()))
        string = "orderno=" + self._order_no + "," + "secret=" + self._secret + "," + "timestamp=" + timestamp
        string = string.encode()
        md5_string = hashlib.md5(string).hexdigest()
        sign = md5_string.upper()
        auth = "sign=" + sign + "&" + "orderno=" + self._order_no + "&" + "timestamp=" + timestamp
        proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
        return proxy, auth

    def _init_headers(self, auth):
        headers = {
            "Proxy-Authorization": auth,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/73.0.3683.75 Safari/537.36"
            }
        return headers

    def _refresh_headers(self):
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
            'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
            'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36']
        user_agent = random.choice(user_agent_list)
        self._headers['User-Agent'] = user_agent

    def visit(self, url):
        """
        访问链接
        :param url:
        :return:
        """
        self._refresh_headers()
        resp = requests.get(url, headers=self._headers, proxies=self._proxy, verify=False, allow_redirects=False,
                            timeout=5)
        if resp.status_code == 200:
            print('访问量+1...')


class Site(metaclass=abc.ABCMeta):
    """
    站点抽象类
    """
    @abc.abstractmethod
    def urls(self):
        yield None


class CSDNSite(Site):
    """
    具体站点实现类, CSDN
    """
    def __init__(self, base_url: str, page):
        """
        :param base_url: 文章列表URL
        :param page: 总页数
        """
        self._base = base_url
        self._page = page
        self._urls = self.get_article_urls()

    def get_article_urls(self, page=1, urls=[]):
        """
        递归获取指定所有页数的文章
        :param page:
        :param urls:
        :return:
        """
        if page > self._page:
            return urls
        url = self._base + '/' + str(page)
        html = self._get_html_text(url)
        if not html:    # 访问超时跳过
            return self.get_article_urls(page+1, urls)
        res = self._parse_url(html)
        urls.extend(res)
        return self.get_article_urls(page+1, urls)

    def _get_html_text(self, url):
        """
        获取网页源码
        :param url:
        :return:
        """
        return requests.get(url).text

    def _parse_url(self, html_text):
        """
        解析网页源码得到每篇文章的链接
        :param html_text:
        :return:
        """
        urls = []
        soup = BeautifulSoup(html_text, 'html.parser')
        articles = soup.findAll('div', {"class": "article-item-box"})
        for article in articles:
            url = article.find_next('a')
            urls.append(url.attrs['href'])
        return urls

    def urls(self):
        """
        url生成器
        :return:
        """
        self._urls.reverse()
        for url in self._urls:
            yield url


class Application:
    """
    主程序
    """
    def __init__(self, visitor: Visitor, site: Site):
        self._v = visitor
        self._site = site

    def run(self):

        while True:
            for url in self._site.urls():
                try:
                    self._v.visit(url)
                except Exception as e:
                    print('访问异常，连接代理服务器失败...')
                    time.sleep(0.2)


if __name__ == '__main__':
    conf = configparser.ConfigParser()
    conf.read('config.ini', 'utf-8-sig')
    base_site = conf.get('conf', 'blog')
    site = CSDNSite(base_site, int(conf.get('conf', 'page')))
    visitor = RequestVisitor(order_no=conf.get('conf', 'order_no'), secret=conf.get('conf', 'secret'))
    app = Application(visitor, site)
    print('开始刷阅读量...')
    for i in range(int(conf.get('conf', 'thread_num'))):
        Thread(target=app.run).start()
