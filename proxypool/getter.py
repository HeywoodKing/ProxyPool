# from proxypool.tester import Tester
from proxypool.db import RedisClient
from proxypool.crawler import Crawler
from proxypool.setting import *
from datetime import datetime
import sys


class Getter(object):
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()
    
    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        """
        # 当值小于0时,不限制reids数量
        if POOL_UPPER_THRESHOLD <= -1:
            return False

        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False
    
    def run(self):
        print('获取器开始执行')
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                try:
                    callback = self.crawler.__CrawlFunc__[callback_label]
                    # 获取代理
                    proxies = self.crawler.get_proxies(callback)
                    sys.stdout.flush()
                    # 将这一批次获取到的代理添加到redis库中
                    for proxy in proxies:
                        if GETTER_PROXY_NO_PORT:
                            self.redis.add(proxy.split(':')[0])
                        else:
                            self.redis.add(proxy)
                except Exception as ex:
                    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '获取器获取代理出现异常：{}，已跳过异常继续执行...'.format(ex))
                    continue
