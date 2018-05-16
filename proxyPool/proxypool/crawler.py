from bs4 import BeautifulSoup
from .utils import get_page
from lxml import etree
import requests
import re
# from pyquery import PyQuery as pq


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_xicidaili(self):
        for i in range(1, 3):
            start_url = 'http://www.xicidaili.com/nn/{}'.format(i)
            html = get_page(start_url)
            if html:
                soup = BeautifulSoup(html, 'lxml')
                ips = soup.find_all('tr')
                for j in range(1, len(ips)):
                    ip_info = ips[j]
                    tds = ip_info.find_all('td')
                    ip = tds[1].text
                    port = tds[2].text
                    yield ':'.join([ip, port])


    def crawl_daili66(self, page_count=5):
        """
        获取代理66
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('正在抓取', url)
            response = requests.get(url)
            html = etree.HTML(response.content.decode("gb2312"))
            if html:
                for i in range(2, 20):
                    ip = html.xpath('//*[@id="main"]/div/div[1]/table/tr[{}]/td[1]/text()'.format(i))
                    port = html.xpath('//*[@id="main"]/div/div[1]/table/tr[{}]/td[2]/text()'.format(i))
                    if not ip:
                        break
                    yield ':'.join([ip[0], port[0]])

    def crawl_yundaili(self):
        """
        云代理
        :return: 代理
        """
        # for page in range(1, 6):
        # 免费代理翻页被关了
        url = 'http://www.ip3366.net/free/?stype=1&page=1'
        print('正在抓取', url)
        # proxies = []
        html = requests.get(url).content.decode("gb2312")
        if html:
            # \s * 匹配空格，起到换行作用
            patt = r"<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>"
            re_ip_address = re.findall(patt, html)
            for ip, port in re_ip_address:
                yield ":".join([ip, port])

    def crawl_liuniandaili(self):
        url = 'http://www.89ip.cn/apijk/?&tqsl=100&sxa=&sxb=&tta=&ports=&ktip=&cf=1'
        print('正在抓取', url)
        html = requests.get(url).text
        if html:
            patt = r"\d+.\d+.\d+.\d+:\d+"
            proxies = re.findall(patt, html)
            for proxy in proxies:
                yield proxy