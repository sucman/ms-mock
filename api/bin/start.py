# 这是程序的入口文件，将启动服务的命令放里面

# 增加根目录为环境变量，方便底层目录执行时目录错误
import sys
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 取到api目录,根目录
sys.path.insert(0, BASE_PATH)

# 加环境变量才能导入，否则导入会异常
from lib.main import server

server.run(port=12030, host='0.0.0.0', debug=True)  # 默认端口号是5000
# host = '0.0.0.0' 代表局域网内别人都可以通ip访问自己的接口
