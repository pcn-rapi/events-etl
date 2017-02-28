from etl.indivisible import main as indivisible
from etl.peoplepower import main as peoplepower

try:
    indivisible.run()
    peoplepower.run()
except ValueError as error:
    print('Caught this error: ' + repr(error))
