from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ToDo(models.Model):

    task = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    creationtime = models.DateTimeField(auto_now_add=True)
    completiontime = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    # to check the author of todos use ForeignKey. It checks id of user which creates tasks.
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # to display titles in admin mode
    def __str__(self):
        return self.task
