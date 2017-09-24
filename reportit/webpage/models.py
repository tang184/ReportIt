# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_markdown.models import MarkdownField
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from webpage.validators import validateURL, validateEmail
# Create your models here.


class Reporter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length = 10, blank=True, null=True)
    phone_number = models.CharField(verbose_name='Phone number(Optional)', max_length=100, blank=True, null=True)
    address = models.CharField(verbose_name='Address(Optional)', max_length=300, blank=True, null=True)
    reporterimg = models.CharField(verbose_name='Reporter Image(Optional)', max_length=300, blank=True, null=True, validators=[validateURL])


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(verbose_name='Phone number', max_length=100)
    address = models.CharField(verbose_name='Address', max_length=300)

    def __str__(self):
        return "address: " + str(self.address)


class Concern(models.Model):

    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    target_agent = models.ManyToManyField(Agent)
    title = models.CharField(max_length=500)
    # content = MarkdownField(blank=False)
    content = models.CharField(max_length=500)

    def __str__(self):
        return str(self.reporter.username) + ", " + self.title