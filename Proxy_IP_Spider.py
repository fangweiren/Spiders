# -*- coding: utf-8 -*-
__author__ = 'Nancy'

from bs4 import BeautifulSoup
import requests
import re
import os
import time
import random
import json


def get_ip_list():
    """
    爬取代理IP
    """
    ip_list = []
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    }
    url = 'http://www.xicidaili.com/nn'
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append('http://' + tds[1].text + ':' + tds[2].text)
    time.sleep(random.uniform(0,3))
    return ip_list

'''
def getqianbailu(url, proxies):
    cookie = '__cfduid=d28ac857dd2e093c6a75be86f78c2f6841516281682; Hm_lvt_e9de253d4210f000b5480ece9919a86b=1516532795,1516533044,1516536144,1516539614; Hm_lpvt_e9de253d4210f000b5480ece9919a86b=1516541160'
    headers = {
    'Cookie': cookie,
    'Connection': 'close',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; W…) Gecko/20100101 Firefox/57.0'
    }
    resp = requests.get(url, headers=headers, proxies=proxies)
    print resp.headers
    html = resp.content.decode("utf-8")
    qianbailu = re.search(r'href="(https.*)"target="_blank"', html)
    if qianbailu:
        return qianbailu.group(1)
    else:
        return
'''

def test_Proxy_Ip(proxies):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    }
    print proxies
    protocol = 'http' if 'http' in proxies.keys() else 'https'
    url = protocol + '://httpbin.org/ip'
    s = requests.Session()
    s.proxies = proxies
    req = s.get(url, headers=headers)
    print 'req', req.content.decode('utf-8')

def check_ip(ip_list):
    User_Agent = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    headers = {
    'User-Agent': random.choice(User_Agent)
    }
    proxy_ip = []
    for ip in ip_list:
        proxy = {'http': ip, 'https': ip}
        if ip_list.index(ip) % 2 == 0:
            url = 'http://2017.ip138.com/ic.asp'
            symbol = True
        else:
            url = 'http://httpbin.org/ip'
            symbol = False
        try:
            res = requests.get(url, proxies=proxy, headers=headers, timeout=3)
            if symbol:
                result = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',res.text)
                if result.group() == ip.split('//')[1].split(':')[0]:
                    print 'success proxy', ip
                    proxy_ip.append(ip)
            else:
                res_ip = json.loads(res.content)['origin']
                if res_ip == ip.split('//')[1].split(':')[0]:
                    print 'success proxy', ip
                    proxy_ip.append(ip)
        except Exception, e:
            pass
        print ip_list.index(ip), len(proxy_ip)
        #time.sleep(random.randint(2,5))
    print proxy_ip

if __name__ == '__main__':
    ip_list = get_ip_list()
    check_ip(ip_list)

'''
while True:
    proxies = get_random_ip(ip_list)
    if os.path.exists('qianbailu.txt'):
        with open('qianbailu.txt', 'r') as f:
            url1 = f.readlines()[-1]
    else:
        url1 = 'https://444av.vip/'
    url2 = 'https://cdn.4006578517.com/newsite.html'
    headers = {
    'Connection': 'close',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; W…) Gecko/20100101 Firefox/57.0'
    }
    try:
        getDailiIp(proxies)

        qianbailu = getqianbailu(url2, proxies)
        print 'qianbailu', qianbailu
        if url1 != qianbailu:
            with open('qianbailu.txt', 'w') as f:
                time1 = time.strftime('%Y-%m-%d %H:%M:%S\n', time.localtime(time.time()))
                f.write(time1)
                f.write(qianbailu)

        break
    except Exception, e:
        print e
        time.sleep(0.5)
'''
