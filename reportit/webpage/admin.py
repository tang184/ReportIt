from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import ReporterProfile
from .models import AgentProfile
<<<<<<< db71c15b78e45736b7b03f84df552ec378016b8e
from .models import Agent
from .models import Concern

admin.site.register(ReporterProfile)
admin.site.register(AgentProfile)
admin.site.register(Agent)
=======
from .models import Concern
>>>>>>> Added basic template for  Concern submission module


admin.site.register(ReporterProfile)
admin.site.register(AgentProfile)
<<<<<<< db71c15b78e45736b7b03f84df552ec378016b8e
admin.site.register(Concern)
=======
admin.site.register(Concern)
>>>>>>> Added basic template for  Concern submission module
