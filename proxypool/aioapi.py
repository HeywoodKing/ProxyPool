
import random
from .db import RedisClient
# from flask import Flask, g, Response, json
from aiohttp import web

__all__ = ['app']

routes = web.RouteTableDef()


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
    # if not hasattr(g, 'redis'):
    #     redis = RedisClient()
    redis = RedisClient()
    return redis


@routes.get('/')
async def index(request):
    return web.Response(text='Welcome to Proxy Pool System')


@routes.get('/count')
async def get_count(request):
    """
    Get the count of proxies
    :param request:
    :return: 代理池总量
    """
    conn = get_conn()
    return web.Response(text=str(conn.count()))


@routes.get('/get')
@routes.get('/proxy')
@routes.get('/random')
async def get_proxy_random(request):
    """
    Get a proxy
    :param request:
    :return: 随机代理
    """
    conn = get_conn()
    return web.Response(text=conn.random())


@routes.get('/pool')
async def get_proxy_pool(request):
    """
    获取代理池中所有的ip列表
    :param request:
    :return:
    """
    conn = get_conn()
    address_list = list(conn.all())
    return web.json_response({'total': len(address_list), 'proxy_ip': address_list})


@routes.get('/max')
async def get_proxy_max(request):
    """
    获取分值最大的ip列表
    :param request:
    :return:
    """
    conn = get_conn()
    address_list = list(conn.max_all())
    return web.json_response({'total': len(address_list), 'proxy_ip': address_list})


@outter
@routes.get('/proxy/{port}')
async def get_proxy_by_port(request):
    """
    获取指定端口的一个ip
    :param request:
    :return:
    """
    port = request.match_info.get('port', 80)
    conn = get_conn()
    address_list = list(conn.all())
    random.shuffle(address_list)
    for address in address_list:
        try:
            proxy_port = address.split(':')[-1]
            if proxy_port == port:
                return web.Response(text=address)
        except Exception as ex:
            print('get_ip_by_port:{}'.format(ex))

    return web.Response(text='')


@outter
@routes.get('/proxy/{start}/{stop}')
async def get_proxy_range(request):
    start = request.match_info.get('start', 0)
    stop = request.match_info.get('stop', 0)
    print('start:{},stop:{}'.format(start, stop))
    return web.Response(text=(start + '/' + stop))


app = web.Application()
app.add_routes(routes)
# app.router.add_routes(routes)
# app.add_routes([
#     web.get('/', index),
#     web.get('/count', get_count),
#     web.get('/random', get_proxy_random),
#     web.get('/get', get_proxy_random),
#     web.get('/proxy', get_proxy_random),
#     web.get('/max', get_proxy_max),
#     web.get('/pool', get_proxy_pool),
#     web.get('/proxy/{port}', get_proxy_by_port),
#     web.get('/proxy/{start}/{stop}', get_proxy_range)
# ])


if __name__ == '__main__':
    web.run_app(app)
