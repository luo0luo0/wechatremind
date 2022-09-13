#!/bin/bash

echo "EXECUTE TIME: " $(date +"%Y-%m-%d %H:%M:%S") >> /home/luo/projects/calendar/run.log

MYSQL_PW=test python /home/luo/projects/calendar/crawler/crawlCalendar.py &>> /home/luo/projects/calendar/run.log
