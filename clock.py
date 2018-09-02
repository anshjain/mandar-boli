import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='thu', hour=12, minute=01)
def scheduled_job():
    print "fdsgjkdjkghdf===="
    subprocess.call('python manage.py recordscsv', shell=True, close_fds=True)

sched.start()