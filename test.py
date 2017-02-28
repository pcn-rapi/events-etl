from etl.indivisible import main as indivisible

try:
    indivisible.run()
except ValueError as error:
    print('Caught this error: ' + repr(error))

try:
    peoplepower.run()
except ValueError as error:
    print('Caught this error: ' + repr(error))
