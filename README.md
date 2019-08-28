# ProxyPool
Using python to build free, practical, efficient, asynchronous, flexible pool of agents for local and remote use, free to switch between databases, designed to create a powerful and easy to use free agent.

使用python搭建免费，实用，高效，异步，灵活的可用于本地和远程的代理池，可自由切换数据库，旨在打造一款功能强大易用的免费代理。

## 环境
```
python3.7
pip19.0.2
pipenv
redis

```

## 安装

### 安装Python
至少Python3.5以上

### 安装Redis服务
安装好之后将Redis服务开启

### 安装虚拟环境
```
pip install pipenv
```

### 使用pipenv安装依赖
##### 依赖环境
```
python3.7
pip19.0.2
pipenv
aiohttp
fastapi[flask]
redis
requests
pyquery

```

### 开发环境部署 
```
pipenv install --dev
```

### 正式环境部署
```
pipenv install --ignore-pipfile
```

### 安装完依赖之后查看
```
pipenv graph
```

### 配置代理池

```
cd proxypool
```

进入proxypool目录，修改settings.py文件

PASSWORD为Redis密码，如果为空，则设置为None


#### 打开代理池和API

```
python3 run.py
```

## 获取代理


利用requests获取方法如下

```python
import requests

PROXY_POOL_URL = 'http://localhost:5555/random'

def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None
```

