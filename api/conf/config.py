DEBUG = True
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'msinfouser'
PASSWORD = 'msinfouser'
HOST = '192.168.9.208'
PORT = 3306
DATABASE = 'ms_info'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT,
                                                                       DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
