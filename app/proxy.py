# _*_coding:utf8_*_
# Project: lin_mass_tools
# File: proxy.py
# Author: ClassmateLin
# Email: 406728295@qq.com
# Time: 2020/2/23 7:54 上午
# DESC:
import abc
import random
import requests
from bs4 import BeautifulSoup
import execjs
import re
import json
import time
import hashlib
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class BaseProxy:
    """
    代理基类
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    }

    def __init__(self, page):
        self._proxies = []
        self._page = page

    def get_one(self):
        """
        随机返回一个代理
        :return:
        """
        if not self._proxies:
            return []
        return random.choice(self._proxies)

    def get_all(self):
        """
        返回所有代理
        :return:
        """
        return self._proxies

    def check_proxy(self, proxy):
        """
        检测代理是否可用
        :return:
        """
        url = 'https://api.ipify.org/?format=json'
        try:
            res = requests.get(url, proxies=proxy, timeout=3).json()
            if 'ip' in res:
                print(res['ip'])
                return True
        except Exception as e:
            return False


class XiCiProxy(BaseProxy):
    """
    西刺代理: http://www.xicidaili.com
    """

    def __init__(self, page=5):
        super().__init__(page)
        self._base_url = 'http://www.xicidaili.com/nn/{}'
        self._proxies = self._get_proxies()

    def _get_proxies(self):
        """
        获取代理IP
        :return:
        """
        proxies = []
        for page in range(1, self._page+1):
            url = self._base_url.format(str(page))
            proxies.extend(self._get_page_proxies(url))
        return proxies

    def _get_page_proxies(self, url):
        """
        获取单个页面的代理IP
        :param url:
        :return:
        """
        proxies = []
        text = requests.get(url, headers=type(self).headers).text
        soup = BeautifulSoup(text, 'html.parser')
        tr_list = soup.findAll('tr', {'class': 'odd'})
        for tr in tr_list:
            country_td = tr.find_next('td', {'class': 'country'})
            ip_td = country_td.find_next('td')
            port_td = ip_td.find_next('td')
            protocol = port_td.find_next('td').find_next('td').find_next('td').text.lower()
            proxy = {
                protocol: '{}://{}:{}'.format(protocol, ip_td.text, port_td.text)
            }
            proxies.append(proxy)
        return proxies


class SixSixProxy(BaseProxy):
    """
    66代理
    """
    def __init__(self, page=10):
        super().__init__(page)
        self._count = page * 10

    def _get_proxies(self, count=100):

        urls = [
            "http://www.66ip.cn/mo.php?sxb=&tqsl={}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=",
            "http://www.66ip.cn/nmtq.php?getnum={}&isp=0&anonymoustype=0&s"
            "tart=&ports=&export=&ipaddress=&area=0&proxytype=2&api=66ip"
        ]
        try:

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
                       'Accept': '*/*',
                       'Connection': 'keep-alive',
                       'Accept-Language': 'zh-CN,zh;q=0.8'}
            session = requests.session()
            src = session.get("http://www.66ip.cn/", headers=headers).text
            src = src.split("</script>")[0] + '}'
            src = src.replace("<script>", "function test() {")
            src = src.replace("while(z++)try{eval(", ';var num=10;while(z++)try{var tmp=')
            src = src.replace(");break}", ";num--;if(tmp.search('cookie') != -1 | num<0){return tmp}}")
            ctx = execjs.compile(src)
            src = ctx.call("test")
            src = src[src.find("document.cookie="): src.find("};if((")]
            src = src.replace("document.cookie=", "")
            src = "function test() {var window={}; return %s }" % src
            cookie = execjs.compile(src).call('test')
            js_cookie = cookie.split(";")[0].split("=")[-1]
        except Exception as e:
            print(e)
            return

        for url in urls:
            try:
                html = session.get(url.format(count), cookies={"__jsl_clearance": js_cookie}, headers=headers).text
                print(html)
                ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", html)
                for ip in ips:
                    proxy = "http://{}".format(ip)
                    self._proxies.append(proxy)
            except Exception as e:
                print(e.args)
                pass


class FreeProxy(BaseProxy):
    """
    免费代理: http://proxylist.fatezero.org/proxy.list
    """
    def __init__(self, page=10):
        super().__init__(page)
        self._proxies = self._get_proxies()

    def _get_proxies(self):
        proxies = []
        url = "http://proxylist.fatezero.org/proxy.list"
        temp_set = set()
        try:
            proxy_list = requests.get(url=url, headers=type(self).headers)
            lines = proxy_list.text.split('\n')
            for i, line in enumerate(lines):
                try:
                    content = json.loads(line)
                except Exception as e:
                    print(e.args)
                    continue
                if content['host'] in temp_set:
                    continue
                proxy = {
                    content['type']: '{}://{}:{}'.format(content['type'], content['host'], content['port'])
                }
                proxies.append(proxy)
                temp_set.add(content['host'])
            return proxies
        except Exception as e:
            print(e.args)
            return []


class QuickProxy(BaseProxy):
    """
    快代理 https://www.kuaidaili.com/
    """
    def __init__(self, page=10):
        """
        :param page:
        """
        super().__init__(page)
        self._base_url = 'https://www.kuaidaili.com/free/inha/{}/'
        self._proxies = self._get_proxies()

    def _get_proxies(self):
        page = 1
        proxies = []
        while page < self._page:
            url = self._base_url.format(str(page))
            html_text = self._get_html_text(url)
            temp_proxies = self._parse_html_text(html_text)
            proxies.extend(temp_proxies)
            page += 1
            time.sleep(0.5)
        return proxies

    def _get_html_text(self, url):
        """
        获取页面文本
        :param url:
        :return:
        """
        try:
            return requests.get(url=url).text
        except Exception as e:
            print(e.args)

    def _parse_html_text(self, text):
        """
        解析网页
        :param text:
        :return:
        """
        if text is None:
            print('text is None!')
            return list()

        proxies = list()
        soup = BeautifulSoup(text, 'html.parser')
        tr_list = soup.find_all('tr')
        for tr in tr_list:
            td_list = tr.find_all_next('td')
            ip = td_list[0].text
            port = td_list[1].text
            protocol = td_list[3].text.strip().lower()
            proxy = {
                protocol: '{}://{}:{}'.format(protocol, ip, port)
            }
            proxies.append(proxy)
        return proxies


class XunProxy:
    """
    讯代理
    """
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

    def __init__(self, order_no='', secret=''):
        """
        :param order_no:
        :param secret:
        """
        self._ip = "forward.xdaili.cn"
        self._port = "80"
        self._ip_port = self._ip + ":" + self._port
        self._order_no = order_no
        self._secret = secret
        self._proxy = {"http": "http://" + self._ip_port, "https": "https://" + self._ip_port}
        self._headers = self._get_headers()

    @property
    def proxy(self):
        """
        返回代理
        :return:
        """
        return self._proxy

    @property
    def headers(self):
        """
        返回请求头
        :return:
        """
        self._headers['user-agent'] = random.choice(type(self).user_agent_list)
        return self._headers

    def _get_headers(self):
        """
        获取请求头
        :return:
        """
        timestamp = str(int(time.time()))
        string = "orderno=" + self._order_no + "," + "secret=" + self._secret + "," + "timestamp=" + timestamp
        string = string.encode()
        md5_string = hashlib.md5(string).hexdigest()
        sign = md5_string.upper()
        auth = "sign=" + sign + "&" + "orderno=" + self._order_no + "&" + "timestamp=" + timestamp
        headers = {
            "Proxy-Authorization": auth,
            "user-agent": random.choice(type(self).user_agent_list)
        }
        return headers

    def test(self, url):
        """
        测试访问
        :param url:
        :return:
        """
        try:
            res = requests.get(url, headers=self._headers,
                               proxies=self._proxy, verify=False, allow_redirects=False, timeout=5)
            if res.status_code == 200:
                return True
        except Exception as e:
            print(e.args)
            return False

    def get_cur_ip(self):
        """
        检测代理是否可用
        :return:
        """
        url = 'https://api.ipify.org/?format=json'
        try:
            res = requests.get(url, headers=self._headers, proxies=self._proxy,
                               verify=False, allow_redirects=False, timeout=5).json()
            if 'ip' in res:
                print(res['ip'])
                return True
        except Exception as e:
            return False


def get(url, headers, proxy):
    """
    :param url
    :param headers:
    :param proxies:
    :return:
    """
    res = requests.get(url, headers=headers, proxies=proxy, verify=False, allow_redirects=False, timeout=5)
    print(res.status_code)


if __name__ == '__main__':
    pro = XunProxy()
    print(pro.get_cur_ip())
    print(pro.test('https://www.baidu.com'))
    get('https://www.baidu.com', pro.headers, pro.proxy)
