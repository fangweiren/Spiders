import time
# import sys
import queue
import threading
import requests
import json
from .db import RedisClient
# from .setting import *

lock = threading.Lock()
TEST_Q = queue.Queue()
RESULT = queue.Queue()


class myThread(threading.Thread):
    def __init__(self):
        super(myThread, self).__init__()  # 调用父类的构造函数
        self.redis = RedisClient()

    def work(self):
        i = 0
        while not TEST_Q.empty():
            proxy = TEST_Q.get()
            lock.acquire()
            print("Processing %d: " % i, proxy)
            lock.release()
            self.test_single_proxy(proxy)
            time.sleep(3)
            TEST_Q.task_done()
            i += 1

    def test_single_proxy(self, proxy):
        """
        测试单个代理
        :param proxy:
        :return:
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }
        lock.acquire()
        print('正在测试', proxy)
        lock.release()
        proxies = {'http': proxy, 'https': proxy}
        # noinspection PyBroadException
        try:
            url = 'http://httpbin.org/ip'
            res = requests.get(url, proxies=proxies, headers=headers, timeout=3)
            res_ip = json.loads(res.content)['origin']
            if res_ip == proxy.split(':')[0]:
                lock.acquire()
                print('代理可用', proxy)
                RESULT.put(proxy)
                lock.release()
            else:
                lock.acquire()
                self.redis.decrease(proxy)
                print('代理无效', proxy)
                lock.release()
            time.sleep(1.5)
        except Exception:
            lock.acquire()
            self.redis.decrease(proxy)
            print('代理请求失败', proxy)
            lock.release()

    def run(self):
        """
        测试主函数
        :return:
        """
        print('测试器开始运行')
        try:
            count = self.redis.count()
            print('当前剩余', count, '个代理')
            for ip in self.redis.all():
                TEST_Q.put(ip)
            all_thread = []
            for _ in range(8):
                t = threading.Thread(target=self.work)
                all_thread.append(t)
                t.start()
            for t in all_thread:
                t.join()
            TEST_Q.join()
        except Exception as e:
            print('测试器发生错误', e.args)