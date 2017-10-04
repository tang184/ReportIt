# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_markdown.models import MarkdownField
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from webpage.validators import validateURL, validateEmail
import django
# Create your models here.


class Reporter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    legal_name = models.CharField(verbose_name='Legal Name', max_length=100)
    gender = models.CharField(max_length = 10, blank=True, null=True)
    phone_number = models.CharField(verbose_name='Phone number(Optional)', max_length=100, blank=True, null=True)
    address = models.CharField(verbose_name='Address(Optional)', max_length=300, blank=True, null=True)
    reporterimg = models.CharField(verbose_name='Reporter Image(Optional)', max_length=300, blank=True,
                                   default="http://127.0.0.1:8000/static/images/default_avatar.png",
                                   validators=[validateURL])
    about = models.CharField(verbose_name='About(Optional)', max_length=300, blank=True, null=True)
    historical_concern_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return str(self.user.username)

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    legal_name = models.CharField(blank=False, verbose_name='Legal Name', max_length=100)
    phone_number = models.CharField(verbose_name='Phone number', max_length=100)
    address = models.CharField(verbose_name='Address', max_length=300)
    agentimage = models.CharField(verbose_name='Agent Badge Logo', max_length=300, validators=[validateURL], default=None)
    agentverifile = models.CharField(verbose_name='Agent verification file', max_length=300, validators=[validateURL], default=None)
    about = models.CharField(verbose_name='About', max_length=300, default=None)

    def __str__(self):
        return str(self.legal_name)


class Concern(models.Model):

    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
    target_agent = models.ManyToManyField(Agent)
    title = models.CharField(max_length=500)
    # content = MarkdownField(blank=False)
    content = models.CharField(max_length=500)

    concern_id = models.IntegerField(default=-1, blank=True) # For now, total count is used as id of concern
    upvote_count = models.IntegerField(default=0)
    isSolved = models.BooleanField(default=False)
    submitted_time = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return str(self.reporter.user.username) + ", " + self.title