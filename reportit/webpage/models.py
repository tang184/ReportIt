# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length = 250)
    password = models.CharField(max_length = 500)
    email = models.CharField(max_length = 100)

    def __str__(self):
        return self.username + '-' + self.email

class ReporterProfile(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    gender = models.CharField(max_length = 10)

class AgentProfile(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)