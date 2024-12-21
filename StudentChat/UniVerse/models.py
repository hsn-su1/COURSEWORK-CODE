from django.db import models
from django.contrib.auth.models import User  # User is the model/table where data is stored

# Create your models here.

# Model(database) to save your messages.

class Message(models.Model):

    from_whom = models.ForeignKey(User, on_delete=models.PROTECT, default=None, related_name="from_user") # A foreign key is a column or columns in one table that references the primary key in another table

    to_whom = models.ForeignKey(User, on_delete=models.PROTECT, default=None, related_name="to_user") # related_name changes name of database as both messages and model share User table

    message = models.TextField()

    date = models.DateField(null=True) # The null=True argument means that the date field in the database is allowed to store NULL values, which represent the absence of data.

    time = models.TimeField(null=True)

    has_been_seen = models.BooleanField(null=True, default=False)

class UserChannel(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None)
    channel_name = models.TextField()