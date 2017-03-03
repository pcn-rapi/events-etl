# from etl.indivisible import main as indivisible
from etl.peoplepower import main as peoplepower

# try:
#     indivisible.run()
# except ValueError as error:
#     print('Caught this error: ' + repr(error))

try:
    peoplepower.run()
except ValueError as error:
    print('Caught this error: ' + repr(error))
