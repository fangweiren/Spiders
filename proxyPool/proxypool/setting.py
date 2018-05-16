# Redis 数据库地址
REDIS_HOST = 'localhost'

# Redis 端口
REDIS_PORT = 6379

# Redis 密码
REDIS_PASSWORD = None

REDIS_KEY = 'proxies'

# 代理分值
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10

VALID_STATUS_CODES = [200, 302]

# 代理池数量界限
POOL_UPPER_THRESHOLD = 10000

# 检查周期
TESTER_CYCLE = 1800
# 获取周期
GETTER_CYCLE = 1000

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 测试 API，建议抓哪个网站测哪个
TEST_URL = 'http://www.baidu.com'

# API 配置
API_HOST = '0.0.0.0'
API_PORT = 5555

# 最大批测试量
BATCH_TEST_SIZE = 10