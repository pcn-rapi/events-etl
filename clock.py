# encoding=utf8

from apscheduler.schedulers.blocking import BlockingScheduler
from etl.peoplepower import main as peoplepower
from etl.indivisible import main as indivisible

from rq import Queue
from worker import conn

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=30)
def timed_for_aclu():
    print('Running Job for ACLU')
    q = Queue(connection=conn)
    result = q.enqueue(peoplepower.queue, timeout=500)

@sched.scheduled_job('interval', minutes=30)
def timed_for_indivisible():
    print('Running Job for Indivisible')
    q = Queue(connection=conn)
    result = q.enqueue(indivisible.queue, timeout=500)

sched.start()
