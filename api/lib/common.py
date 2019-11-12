#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

"""
@author:
"""
from datetime import datetime
from datetime import timedelta


def get_hourly_chime(dt, step=0, rounding_level="s"):
    """
    计算整分钟，整小时，整天的时间
    :param step: 往前或往后跳跃取整值，默认为0，即当前所在的时间，正数为往后，负数往前。
                例如：
                step = 0 时 2019-04-11 17:38:21.869993 取整秒后为 2019-04-11 17:38:21
                step = 1 时 2019-04-11 17:38:21.869993 取整秒后为 2019-04-11 17:38:22
                step = -1 时 2019-04-11 17:38:21.869993 取整秒后为 2019-04-11 17:38:20
    :param rounding_level: 字符串格式。
                "s": 按秒取整；"min": 按分钟取整；"hour": 按小时取整；"days": 按天取整
    :return: 整理后的时间戳
    """
    if rounding_level == "days":  # 整天
        td = timedelta(days=-step, seconds=dt.second, microseconds=dt.microsecond, milliseconds=0, minutes=dt.minute,
                       hours=dt.hour, weeks=0)
        new_dt = dt - td
    elif rounding_level == "hour":  # 整小时
        td = timedelta(days=0, seconds=dt.second, microseconds=dt.microsecond, milliseconds=0, minutes=dt.minute,
                       hours=-step, weeks=0)
        new_dt = dt - td
    elif rounding_level == "min":  # 整分钟
        td = timedelta(days=0, seconds=dt.second, microseconds=dt.microsecond, milliseconds=0, minutes=-step, hours=0,
                       weeks=0)
        new_dt = dt - td
    elif rounding_level == "s":  # 整秒
        td = timedelta(days=0, seconds=-step, microseconds=dt.microsecond, milliseconds=0, minutes=0, hours=0, weeks=0)
        new_dt = dt - td
    else:
        new_dt = dt
    timestamp = new_dt.timestamp()  # 对于 python 3 可以直接使用 timestamp 获取时间戳
    # timestamp = (new_dt - datetime.fromtimestamp(0)).total_seconds()  # Python 2 需手动换算
    return timestamp
