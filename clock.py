# encoding=utf8

from apscheduler.schedulers.blocking import BlockingScheduler
from etl.peoplepower import main as peoplepower

from rq import Queue
from worker import conn


sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print(' This job runs every 3 minutes')
    q = Queue(connection=conn)
    result = q.enqueue(peoplepower.queue)

sched.start()
