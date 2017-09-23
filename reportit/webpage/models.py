# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_markdown.models import MarkdownField
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(verbose_name='Phone number', max_length=100)
    address = models.CharField(verbose_name='Address', max_length=300)

    def __str__(self):
        return "address: " + str(self.address)

class ReporterProfile(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    gender = models.CharField(max_length = 10)

class AgentProfile(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)

class Concern(models.Model):

    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    target_agent = models.ManyToManyField(AgentProfile)
    title = models.CharField(max_length=500)
    # content = MarkdownField(blank=False)
    content = models.CharField(max_length=500)

    def __str__(self):
        return str(self.reporter.username) + ", " + self.title