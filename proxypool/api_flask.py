
import random
from flask import Flask, g, Response, json
from .db import RedisClient

__all__ = ['app']

app = Flask(__name__)


# 打印获取到的代理
# 无固定参数带返回值的装饰器
def outter(func):
    def inner(*args, **kwargs):
        import sys
        import time
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000
        print("time is %d ms" % execution_time)
        print('\b 取到随机代理：{}'.format(res), end='', flush=True,)
        sys.stdout.flush()
        return res

    return inner


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool System</h2>'


@app.route('/count')
def get_counts():
    """
    Get the count of proxies
    :return: 代理池总量
    """
    conn = get_conn()
    return str(conn.count())


@app.route('/proxy')
@app.route('/get')
@app.route('/random')
def get_proxy():
    """
    Get a proxy
    :return: 随机代理
    """
    conn = get_conn()
    return conn.random()


@app.route('/pool')
def get_proxy_all():
    """
    获取代理池中所有的ip列表
    :return:
    """
    conn = get_conn()
    address_list = list(conn.all())
    return Response(json.dumps({'total': len(address_list), 'proxy_ip': address_list}), content_type='application/json')


@app.route('/max')
def get_proxy_max_ips():
    """
    获取分值最大的ip列表
    :return:
    """
    conn = get_conn()
    address_list = list(conn.max_all())
    return Response(json.dumps({'total': len(address_list), 'proxy_ip': address_list}), content_type='application/json')


@outter
@app.route('/proxy/<port>')
def get_proxy_by_port(port):
    """
    获取指定端口的一个ip
    :param port:
    :return:
    """
    conn = get_conn()
    address_list = list(conn.all())
    random.shuffle(address_list)
    for address in address_list:
        try:
            proxy_port = address.split(':')[-1]
            if proxy_port == port:
                return address
        except Exception as ex:
            print('get_ip_by_port:{}'.format(ex))


@outter
@app.route('/proxy/<start>/<stop>')
def get_proxy_range(start, stop):
    print('start:{},stop:{}'.format(start, stop))
    return start + '/' + stop


if __name__ == '__main__':
    app.run()
