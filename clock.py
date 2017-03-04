# encoding=utf8

from apscheduler.schedulers.blocking import BlockingScheduler
from etl.peoplepower import main as peoplepower

from rq import Queue
from worker import conn

q = Queue(connection=conn)
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=60)
def timed_job():
    print(' This job runs every 60 minutes')
    result = q.enqueue(peoplepower.queue)

sched.start()
