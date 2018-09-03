import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('cron', day='3', hour=23, minute=30)
def scheduled_job():
    print "Start con"
    subprocess.call('python ./manage.py recordscsv', shell=True, close_fds=True)

sched.start()