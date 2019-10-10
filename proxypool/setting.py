# Redis数据库地址
REDIS_HOST = '192.168.1.141'
# Redis端口
REDIS_PORT = 6379
# Redis密码，如无填None
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'

# # Redis数据库地址
# REDIS_HOST = '121.201.107.56'
# # Redis端口
# REDIS_PORT = 6377
# # Redis密码，如无填None
# REDIS_PASSWORD = 'whbvybui789214^%&NJcn2jmci208U980ui21803uf0jhv02jh098hvnhu2jh938ASDEF2324Cdgrv'
# REDIS_KEY = 'proxies'


# 代理分数
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
# 检测ip有效无效的分值调节阈
ADJUST_SCORE = -20

VALID_STATUS_CODES = [200, 302]

# 代理池数量界限
POOL_UPPER_THRESHOLD = 5000

# 检查周期(秒)，默认20秒检测一遍代理池IP是否可用
TESTER_CYCLE = 20
# 获取周期(秒)，默认10分钟，抓取一次代理IP
GETTER_CYCLE = 60*20

# 测试API，建议抓哪个网站测哪个
TEST_URL = 'http://www.baidu.com'

# API配置
API_HOST = '192.168.1.79'
API_PORT = 5555
# aiohttp | fastapi | flask | vibora
API_SOURCE = 'flask'

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 最大批测试量
BATCH_TEST_SIZE = 100
