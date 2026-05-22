from django.contrib import admin

from .models import Vessel, Voyage, TelemetryRecord, OperationalAlert

admin.site.register(Vessel)
admin.site.register(Voyage)
admin.site.register(TelemetryRecord)
admin.site.register(OperationalAlert)

