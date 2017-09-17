from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import User
from .models import ReporterProfile
from .models import AgentProfile


admin.site.register(User)
admin.site.register(ReporterProfile)
admin.site.register(AgentProfile)
