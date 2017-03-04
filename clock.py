# encoding=utf8

from apscheduler.schedulers.blocking import BlockingScheduler
from etl.peoplepower import main as peoplepower


sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=60)
def timed_job():
    print(' This job runs every 60 minute')
    try:
        peoplepower.run()
    except ValueError as error:
        print('Caught this error: ' + repr(error))


sched.start()
