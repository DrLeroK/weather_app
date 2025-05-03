from django.db import models
# Imports Django's models module which contains the base Model class and all the 
# field types needed to create database models.

from django.contrib import auth
# Imports Django's authentication framework (auth).


# Create your models here.
class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        return "@{}".format(self.username)



# superuser = hp7
