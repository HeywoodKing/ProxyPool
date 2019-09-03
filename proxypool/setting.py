# Redis数据库地址
REDIS_HOST = '192.168.1.141'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = None

REDIS_KEY = 'proxies'

# 代理分数
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
# 检测ip有效无效的分值调节值
ADJUST_SCORE = -20

VALID_STATUS_CODES = [200, 302]

# 代理池数量界限
POOL_UPPER_THRESHOLD = 5000

# 检查周期(秒)
TESTER_CYCLE = 20
# 获取周期(秒)
GETTER_CYCLE = 60*30

# 测试API，建议抓哪个网站测哪个
TEST_URL = 'http://www.baidu.com'

# API配置
API_HOST = '192.168.1.79'
API_PORT = 4444

# 开关
TESTER_ENABLED = False
GETTER_ENABLED = False
API_ENABLED = True

# 最大批测试量
BATCH_TEST_SIZE = 100
