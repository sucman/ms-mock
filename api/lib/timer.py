import schedule
import time
from lib.main import set_trade_value


def set_data_timer():
    # 每小时执行一次
    # schedule.every().hour.do(set_trade_value)
    schedule.every().day.at("10:00").do(set_trade_value)
    schedule.every().day.at("11:00").do(set_trade_value)
    schedule.every().day.at("12:00").do(set_trade_value)
    schedule.every().day.at("13:00").do(set_trade_value)
    schedule.every().day.at("14:00").do(set_trade_value)
    schedule.every().day.at("15:00").do(set_trade_value)
    schedule.every().day.at("16:00").do(set_trade_value)
    schedule.every().day.at("17:00").do(set_trade_value)
    schedule.every().day.at("18:00").do(set_trade_value)
    schedule.every().day.at("19:00").do(set_trade_value)
    while True:
        schedule.run_pending()
        time.sleep(1)
