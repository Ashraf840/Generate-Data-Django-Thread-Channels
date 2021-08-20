from django.db import models
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.TextField(max_length=100)
    is_seen = models.BooleanField(default=False)
    
    # Instead of using signals, create 'save' method, so that whenever a model-obj (an obj of 'Notification' model) gets created, 
    # the 'save' method gets called.
    def save(self, *args, **kwargs):
        # print('Save called') # Testing

        # send the obj-data to frontend using channels, whenever a model-obj gets created. (Synchronous-Websocket-Consumer)
        channel_layers = get_channel_layer() # get all channel_layers
        notification_objs_unseen = Notification.objects.filter(is_seen=False).count() + 1   # it's counted the emtpy database while simultaneouly inseted a data [at the beginning when the DB is empty]; otherwise the count-method starts counting from index 1.
        data = {
            'unseen_notificaion_count': notification_objs_unseen,
            'current_notification': self.notification,
        }

        # Whenever we want to send data from any backend's model/ view, we need to use "group_send"
        async_to_sync(channel_layers.group_send)(
            'test_consumer_group', # specify the group-name 
            {
                'type': 'send_nofication',  # calling a consumer-method
                'value': json.dumps(data)   # Converts a python-dict into json-obj
            }
        )

        super(Notification, self).save(*args, **kwargs)


class Students(models.Model):
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField(max_length=100)
    address = models.CharField(max_length=100)
    age = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Student'

    def __str__(self) -> str:
        return self.student_name
