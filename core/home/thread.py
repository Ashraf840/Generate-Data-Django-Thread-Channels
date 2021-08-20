import threading
from .models import *
from faker import Faker
import random, time
from asgiref.sync import async_to_sync

fake = Faker()

# By using 'Thread', the expensive-task can be run in the background, but the html-page load-completion will not get lagged/ affected.
# Means that the html-page will not wait for the background task to be completed fully to get loaded in the browser.
# Making the frontend independent from the backend-task.
# Threading a class-template which includes specific method/s, that is/ are meant to be executed when this 'Thread' class gets called.

# [Purpose]: populate data into backend whenever this thread is called; simultaneously send the each populated current-data into the consumer-group.
class CreateStudentsThread(threading.Thread):
    def __init__(self, total):
        self.total = total  # class-scoped variable; this class accepts an integer-param
        threading.Thread.__init__(self)

    # we can't use async-methods in a "Thread" class
    # [
    #  "creating dummy-data-row in the DB",
    #  "also simultaneously sends that each data to the channel-consumer-group immedietly"
    # ]
    def run(self):
        try:
            print('Thread execution started!')
            current_total = 0
            for i in range(self.total):
                # print(i)

                current_total += 1
                
                # create s single student-record db-query; which is saved in a variable ("stud_obj")
                stud_obj = Students.objects.create(
                    student_name = fake.name(),
                    student_email = fake.email(),
                    address = fake.address(),
                    age = random.randint(10, 50),
                )

                # generate data
                # data = { 'count': i }

                # fetch the currently created single-student-data (grabs from 'stud_obj') & store into this data-dict; 
                data = {
                    'total_num': self.total, # the num which is passed from the view as param
                    'total_inserted_data': current_total, # increasing the toatl-num everytime
                    'student_id': current_total,
                    'student_name': stud_obj.student_name,
                    'student_email': stud_obj.student_email,
                    'student_address': stud_obj.address,
                    'student_age': stud_obj.age,
                }

                print('%s. %s' % (i, data))

                # send data to the channel-consumer-group (Asynchronous-Websocket-Consumer)
                # Send message to room group (in the redis-server)
                channel_layers = get_channel_layer() # get all channel_layers
                async_to_sync(channel_layers.group_send)(
                    'new_consumer_group', # specify the group-name 
                    {
                        'type': 'send_nofication',  # calling a receiver-consumer-method
                        'value': json.dumps(data)   # Converts a python-dict into json-obj
                    }
                )

                # time.sleep(1)

        except Exception as e:
            print(e)
