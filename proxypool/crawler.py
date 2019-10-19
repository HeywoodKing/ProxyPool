# import json
import re
import time
from .utils import get_page
from pyquery import PyQuery as pq
from lxml import etree


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
        """
        执行抓取代理IP方法，返回这一批次的代理列表
        :param callback:
        :return: 返回这一批次的代理列表
        """
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=5):
        """
        获取66代理
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url=url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    address = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    # result = address + ':' + port
                    yield ':'.join([address, port])

    # # 5.66免费代理
    # def crawl_66ip(self):
    #     print('开始抓取---{}......'.format('66免费代理'))
    #     base_url = 'http://www.66ip.cn/mo.php?sxb=&tqsl={}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=http%3A%2F%2Fwww.66ip.cn%2F%3Fsxb%3D%26tqsl%3D1000%26ports%255B%255D2%3D%26ktip%3D%26sxa%3D%26radio%3Dradio%26submit%3D%25CC%25E1%2B%2B%25C8%25A1'
    #     url = base_url.format(4000)
    #     try:
    #         html = get_page(url=url)
    #         if html:
    #             items = re.findall(r"(\d+.\d+.\d+.\d+:\d+)", html)
    #             for result in items:
    #                 yield result.replace(' ', '')
    #
    #     except Exception as ex:
    #         print('{}抓取出错: {}'.format('66免费代理', ex))

    def crawl_kuaidaili(self, page_count=5):
        """
        获取快代理
        :return:
        """
        for page in range(1, page_count + 1):
            url = 'http://www.kuaidaili.com/free/inha/{}/'.format(page)
            html = get_page(url=url)
            if html:
                ip_address = re.compile('<td data-title="IP">(.*?)</td>')
                re_ip_address = ip_address.findall(html)
                port = re.compile('<td data-title="PORT">(.*?)</td>')
                re_port = port.findall(html)
                for address, port in zip(re_ip_address, re_port):
                    result = address + ':' + port
                    yield result.replace(' ', '')

    # def _crawl_kuaidaili(self):
    #     headers = {
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #         'Accept-Encoding': 'gzip, deflate, br',
    #         'Accept-Language': 'zh-CN,zh;q=0.9',
    #         'Cache-Control': 'max-age=0',
    #         'Connection': 'keep-alive',
    #         'Cookie': '_ga=GA1.2.1534667437.1543414963; channelid=0; sid=1557755091348842; _gid=GA1.2.561500697.1557755107; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1557755108; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1557755108',
    #         'Host': 'www.kuaidaili.com',
    #         'Referer': 'https://www.kuaidaili.com/free/2',
    #         'Upgrade-Insecure-Requests': '1',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    #     }
    #     print('开始抓取---{}......'.format('快代理'))
    #     for page_index in range(1, 50):
    #         try:
    #             url = 'https://www.kuaidaili.com/free/inha/{}'.format(page_index)
    #             content = self.get_response(url=url, headers=headers)
    #             root = etree.HTML(content)
    #             rows = root.xpath("//div[@id='list']/table//tr")
    #             for row in rows[1:]:
    #                 server = row.xpath("string(./td[1])")
    #                 port = row.xpath("string(./td[2])")
    #                 server_port = server + ':' + port
    #                 # print(server_port)
    #                 self.redis_client.sadd(self.proxy_key, server_port)
    #
    #         except Exception as ex:
    #             print('{}抓取出错: {}'.format('快代理', ex))
    #         time.sleep(1)

    def crawl_xicidaili(self, page_count=5):
        """
        获取西刺代理
        :return:
        """
        for page in range(1, page_count + 1):
            url = 'http://www.xicidaili.com/nn/{}'.format(page)
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWRjYzc5MmM1MTBiMDMzYTUzNTZjNzA4NjBhNWRjZjliBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUp6S2tXT3g5a0FCT01ndzlmWWZqRVJNek1WanRuUDBCbTJUN21GMTBKd3M9BjsARg%3D%3D--2a69429cb2115c6a0cc9a86e0ebe2800c0d471b3',
                'Host': 'www.xicidaili.com',
                'Referer': 'http://www.xicidaili.com/nn/3',
                'Upgrade-Insecure-Requests': '1',
            }
            html = get_page(url=url, options=headers)
            if html:
                find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
                trs = find_trs.findall(html)
                for tr in trs:
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(tr)
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(tr)
                    for address, port in zip(re_ip_address, re_port):
                        result = address + ':' + port
                        yield result.replace(' ', '')

    # # 3.西刺代理
    # def crawl_xici(self):
    #     print('开始抓取---{}......'.format('西刺代理'))
    #     headers = {
    #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
    #     }
    #     for page in range(1, 50):
    #         try:
    #             url = 'http://www.xicidaili.com/nn/{}'.format(page)
    #             html = get_page(url=url, options=headers)
    #             if html:
    #                 root = etree.HTML(html)
    #                 rows = root.xpath("//table[@id='ip_list']//tr")
    #                 for row in rows[1:]:
    #                     server = row.xpath('normalize-space(td[2])')
    #                     port = row.xpath('normalize-space(./td[3])')
    #                     result = server + ':' + port
    #                     yield result.replace(' ', '')
    #
    #         except Exception as ex:
    #             print('{}抓取出错: {}'.format('西刺代理', ex))
    #         time.sleep(1)

    def crawl_ip3366(self, page_count=5):
        """
        获取ip3366
        :return:
        """
        for page in range(1, page_count + 1):
            url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
            html = get_page(url=url)
            ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            # \s * 匹配空格，起到换行作用
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address + ':' + port
                yield result.replace(' ', '')

    # def crawl_ip3366(self):
    #     """
    #     获取ip3366
    #     :return:
    #     """
    #     for page in range(1, 4):
    #         start_url = 'http://www.ip3366.net/?stype=1&page={}'.format(page)
    #         html = get_page(start_url)
    #         if html:
    #             find_tr = re.compile('<tr>(.*?)</tr>', re.S)
    #             trs = find_tr.findall(html)
    #             for s in range(1, len(trs)):
    #                 find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
    #                 re_ip_address = find_ip.findall(trs[s])
    #                 find_port = re.compile('<td>(\d+)</td>')
    #                 re_port = find_port.findall(trs[s])
    #                 for address, port in zip(re_ip_address, re_port):
    #                     result = address + ':' + port
    #                     yield result.replace(' ', '')

    # # 7.云代理
    # def crawl_ip3366(self):
    #     print('开始抓取---{}......'.format('云代理'))
    #     for page in range(1, 20):
    #         url = 'http://www.ip3366.net/?stype=1&page={}'.format(page)
    #         try:
    #             html = get_page(url=url, )
    #             if html:
    #                 find_tr = re.compile('<tr>(.*?)</tr>', re.S)
    #                 trs = find_tr.findall(html)
    #                 for s in range(1, len(trs)):
    #                     find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
    #                     re_ip_address = find_ip.findall(trs[s])
    #                     find_port = re.compile('<td>(\d+)</td>')
    #                     re_port = find_port.findall(trs[s])
    #                     for address, port in zip(re_ip_address, re_port):
    #                         result = address + ':' + port
    #                         yield result.replace(' ', '')
    #
    #         except Exception as ex:
    #             print('{}抓取出错: {}'.format('云代理', ex))
    #         time.sleep(1)

    def crawl_iphai(self):
        """
        获取ip海代理
        :return:
        """
        url = 'http://www.iphai.com/'
        html = get_page(url=url)
        if html:
            find_tr = re.compile('<tr>(.*?)</tr>', re.S)
            trs = find_tr.findall(html)
            for s in range(1, len(trs)):
                find_ip = re.compile('<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>', re.S)
                re_ip_address = find_ip.findall(trs[s])
                find_port = re.compile('<td>\s+(\d+)\s+</td>', re.S)
                re_port = find_port.findall(trs[s])
                for address, port in zip(re_ip_address, re_port):
                    result = address + ':' + port
                    yield result.replace(' ', '')

    # # 8.ip海
    # def crawl_iphai(self):
    #     print('开始抓取---{}......'.format('ip海'))
    #     start_url = 'http://www.iphai.com/'
    #     try:
    #         html = get_page(start_url, )
    #         if html:
    #             find_tr = re.compile('<tr>(.*?)</tr>', re.S)
    #             trs = find_tr.findall(html)
    #             for s in range(1, len(trs)):
    #                 find_ip = re.compile('<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>', re.S)
    #                 re_ip_address = find_ip.findall(trs[s])
    #                 find_port = re.compile('<td>\s+(\d+)\s+</td>', re.S)
    #                 re_port = find_port.findall(trs[s])
    #                 for address, port in zip(re_ip_address, re_port):
    #                     result = address + ':' + port
    #                     yield result.replace(' ', '')
    #
    #     except Exception as ex:
    #         print('{}抓取出错: {}'.format('ip海', ex))

    def crawl_data5u(self):
        """
        获取data5u代理
        :return:
        """
        url = 'http://www.data5u.com/index.shtml'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID=47AA0C887112A2D83EE040405F837A86',
            'Host': 'www.data5u.com',
            'Referer': 'http://www.data5u.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        }
        html = get_page(url=url, options=headers)
        if html:
            ip_address = re.compile('<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?>(\d+)</li>', re.S)
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address + ':' + port
                yield result.replace(' ', '')

    # # 9.无忧代理
    # def crawl_data5u(self):
    #     print('开始抓取---{}......'.format('无忧代理'))
    #     url = 'http://www.data5u.com/free/gngn/index.shtml'
    #     headers = {
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #         'Accept-Encoding': 'gzip, deflate',
    #         'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    #         'Cache-Control': 'max-age=0',
    #         'Connection': 'keep-alive',
    #         'Cookie': 'JSESSIONID=47AA0C887112A2D83EE040405F837A86',
    #         'Host': 'www.data5u.com',
    #         'Referer': 'http://www.data5u.com/free/index.shtml',
    #         'Upgrade-Insecure-Requests': '1',
    #         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    #     }
    #     try:
    #         html = get_page(url=url, options=headers)
    #         if html:
    #             ip_address = re.compile('<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?>(\d+)</li>',
    #                                     re.S)
    #             re_ip_address = ip_address.findall(html)
    #             for address, port in re_ip_address:
    #                 result = address + ':' + port
    #                 yield result.replace(' ', '')
    #
    #     except Exception as ex:
    #         print('{}抓取出错: {}'.format('无忧代理', ex))

    # 2019-08-27 31代理网站已关闭
    # def crawl_31f(self):
    #     print('开始抓取---三一代理......')
    #     urls = ['http://31f.cn/http-proxy/', 'http://31f.cn/https-proxy/']
    #     for url in urls:
    #         try:
    #             html = get_page(url=url)
    #             if html:
    #                 root = etree.HTML(html)
    #                 rows = root.xpath("//table[@class='table table-striped']/tr")
    #                 for row in rows[1:]:
    #                     address = row.xpath("string(./td[2])")
    #                     port = row.xpath("string(./td[3])")
    #                     result = address + ':' + port
    #                     yield result.replace(' ', '')
    #
    #         except Exception as ex:
    #             print('{}抓取出错: {}'.format('三一代理', ex))

    # 4.89免费代理
    def crawl_89ip(self):
        print('开始抓取---{}......'.format('89免费代理'))
        url = 'http://www.89ip.cn/tqdl.html?api=1&num={}&port=&address=&isp='.format(6000)
        try:
            html = get_page(url=url)
            if html:
                items = re.findall(r"(\d+.\d+.\d+.\d+:\d+)", html)
                for result in items:
                    yield result.replace(' ', '')

        except Exception as ex:
            print('{}抓取出错: {}'.format('89免费代理', ex))

    # 6.神鸡代理
    def crawl_shenji(self):
        print('开始抓取---{}......'.format('神鸡代理'))
        url = 'http://www.shenjidaili.com/open/'
        try:
            html = get_page(url=url)
            if html:
                root = etree.HTML(html)
                rows = root.xpath('//div[@id="pills-stable_https"]/table//tr')
                for row in rows[1:]:
                    result = row.xpath('normalize-space(./td[1])')
                    yield result.replace(' ', '')

        except Exception as ex:
            print('{}抓取出错: {}'.format('神鸡代理', ex))

    # 10.西拉免费代理
    def crawl_xiladaili(self, page_count=10):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'Hm_lvt_31dfac66a938040b9bf68ee2294f9fa9=1557797914; Hm_lpvt_31dfac66a938040b9bf68ee2294f9fa9=1557797914',
            'Host': 'www.xiladaili.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',

        }
        print('开始抓取---{}......'.format('西拉免费代理'))
        for page in range(1, page_count + 1):
            url = 'http://www.xiladaili.com/gaoni/{}'.format(page)
            # response = requests.get(url=url,headers=headers)
            # root = etree.HTML(response.text)
            try:
                html = get_page(url=url, options=headers)
                if html:
                    root = etree.HTML(html)
                    items = root.xpath('//table[@class="fl-table"]/tbody/tr')

                    for item in items:
                        result = item.xpath('normalize-space(./td[1])')
                        yield result.replace(' ', '')

            except Exception as ex:
                print('{}抓取出错: {}'.format('西拉免费代理', ex))
            time.sleep(1)

    # 11.极速代理
    def crawl_superfastip(self, page_count=10):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': 'ci_session=3i2tp5sgeq98v0hgdeq15cqjjjk2qdli; BAEID=C0E983951B3BB836BCB8167238B02B2F; Hm_lvt_3d5b18923ef9442d1616352471891f0d=1557799254; Hm_lpvt_3d5b18923ef9442d1616352471891f0d=1557799418',
            'Host': 'www.superfastip.com',
            'Referer': 'http://www.superfastip.com/welcome/freeip/2',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',

        }
        print('开始抓取---{}......'.format('极速代理'))
        for page in range(1, page_count + 1):
            url = 'http://www.superfastip.com/welcome/freeIP/{}'.format(page)

            # response = requests.get(url=url,headers=headers)
            # root = etree.HTML(response.text)
            try:
                html = get_page(url=url, options=headers)
                if html:
                    root = etree.HTML(html)
                    items = root.xpath('//table[@class="table text-center "]/tbody/tr')
                    for item in items[3:]:
                        address = item.xpath('normalize-space(./td[1])')
                        port = item.xpath('normalize-space(./td[2])')
                        result = address + ":" + port
                        yield result.replace(' ', '')

            except Exception as ex:
                print('{}抓取出错: {}'.format('极速代理', ex))
            time.sleep(1)

    # 12.尼玛代理
    def crawl_nimadaili(self, page_count=10):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'Hm_lvt_3ed2bb1e16717ce82856f570020e6ede=1557801872; Hm_lpvt_3ed2bb1e16717ce82856f570020e6ede=1557801884',
            'Host': 'www.nimadaili.com',
            'Referer': 'http://www.nimadaili.com/gaoni/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
        }
        print('开始抓取---{}......'.format('泥马代理'))
        for page in range(1, page_count + 1):
            url = 'http://www.nimadaili.com/gaoni/{}/'.format(page)
            try:
                html = get_page(url=url, options=headers)
                if html:
                    root = etree.HTML(html)
                    items = root.xpath('//table[@class="fl-table"]/tbody/tr')
                    for item in items:
                        result = item.xpath('normalize-space(./td[1])')
                        yield result.replace(' ', '')

            except Exception as ex:
                print('{}抓取出错: {}'.format('尼玛代理', ex))
            time.sleep(1)

    # # 13.极光代理
    # def crawl_jiguangdaili(self, page_count=10):
    #     pass
