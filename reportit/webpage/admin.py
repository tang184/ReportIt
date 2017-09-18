from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import ReporterProfile
from .models import AgentProfile
from .models import Concern


admin.site.register(ReporterProfile)
admin.site.register(AgentProfile)
admin.site.register(Concern)