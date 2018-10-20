#!/usr/bin/env python

import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('cron', day='20', hour=10, minute=25)
def record_csv_job():
    print ("Start con")
    subprocess.call('python ./manage.py recordscsv', shell=True, close_fds=True)


# @sched.scheduled_job('cron', day='9', hour=13, minute=30)
# def send_reminder_job():
#     print ("Start send message con!")
#     subprocess.call('python ./manage.py sendmessage', shell=True, close_fds=True)


sched.start()