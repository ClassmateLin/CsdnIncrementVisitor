# _*_coding:utf8_*_
# Project: lin_mass_tools
# File: article.py
# Author: ClassmateLin
# Email: 406728295@qq.com
# Time: 2020/2/23 7:53 上午
# DESC:
import abc
import requests
import random
from bs4 import BeautifulSoup


class Article(metaclass=abc.ABCMeta):
    """
    文章抽象类
    """

    @abc.abstractmethod
    def get_all(self):
        """
        获取所有文章
        :return:
        """
        pass

    @abc.abstractmethod
    def get_one(self):
        """
        获取一篇文章
        :return:
        """
        pass


class CSDNArticle(Article):
    """
    爬取CSDN文章的链接
    """

    headers = {
        'referer': 'https://www.baidu.com',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    }

    user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/27.0.1453.116 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        ' Chrome/32.0.1667.0 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko)'
        ' Chrome/27.0.1453.116 Safari/537.36']

    def __init__(self, blog_name='ClassmateLin'):

        self._base_url = 'https://blog.csdn.net/{}/article/list/'.format(blog_name)
        self._article = self._get_articles()

    def get_all(self):
        """
        返回所有文章
        :return:
        """
        return self._article

    def get_one(self):
        """
        随机返回一篇文章
        :return:
        """
        return random.choice(self._article)

    def _get_articles(self):
        """
        获取所有文章
        :return:
        """
        articles = []
        page = 1

        while True:  # 穷举所有页数的文章，直到没有文章为止
            url = self._base_url + str(page)    # 第page的文章列表
            html_text = self._get_article_page_html(url, page)
            arts = self._parse_articles(html_text)
            if len(arts) == 0:
                break
            articles.extend(arts)
            page += 1

        return articles

    def _get_article_page_html(self, url, page):
        """
        获取html文本的数据
        :param url:
        :return:
        """
        if page > 1:  # 第一页的referer是百度，后续是上一页
            type(self).headers['referer'] = self._base_url + str(page-1)

        # 切换user-agent
        type(self).headers['user-agent'] = random.choice(type(self).user_agent_list)

        html_text = requests.get(url=url, headers=type(self).headers).text

        return html_text

    def _parse_articles(self, html_text):
        """
        解析网页源码得到每篇文章的标题丶链接丶阅读量
        :param html_text:
        :return:
        """
        arts = []
        soup = BeautifulSoup(html_text, 'html.parser')
        articles = soup.findAll('div', {"class": "article-item-box"})  # 文章均包裹在一个div里面，如果没有文章这里是空的。
        for art in articles:
            tag_a = art.find_next('a')  # 搜索a标签
            url = tag_a.attrs['href']   # 文章链接
            read_num = int(art.find_next('span', {'class': 'num'}).text)  # 文章阅读数量
            title = tag_a.text.replace('\n', '')  # 文章标题
            arts.append({
                'title': title,
                'url': url,
                'read_num': read_num
            })
        return arts


if __name__ == '__main__':
    article = CSDNArticle()
    article.get_one()