#! /bin/bash
nohup python3 start.py >/dev/null 2>&1 &
command > /opt/app/ms-mock/api/logs/catalina.out