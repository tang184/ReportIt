from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.


from .models import Reporter, Agent, Concern, File

admin.site.register(Reporter)
admin.site.register(Agent)
admin.site.register(Concern)
admin.site.register(File)
