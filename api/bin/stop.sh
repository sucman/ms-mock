#!/bin/sh

ps -ef|grep python3|grep -v grep|awk '{print $2}' | while read pid

do
    echo "tomcat is running, to kill bootstrap pid=$pid"
    kill -9 $pid
    echo "kill result: $?"
done