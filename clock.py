# encoding=utf8

from apscheduler.schedulers.blocking import BlockingScheduler
from etl.peoplepower import main as peoplepower

from rq import Queue
from worker import conn

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=60)
def timed_job():
    print(' This job runs every 60 minutes')
    q = Queue(connection=conn)
    result = q.enqueue(peoplepower.queue)
    print('Result is %d ' % result)
    result2 = q.enqueue(indivisible.queue)
    print('Result2 is %d ' % result2)

sched.start()
