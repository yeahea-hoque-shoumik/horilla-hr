"""
Register models with the Django admin site.

This section of code registers the BiometricDevices and BiometricEmployees models
with the Django admin site, allowing them to be managed via the admin interface.

"""

from django.contrib import admin

from .models import (
    BiometricDevices,
    BiometricEmployees,
    BiometricPushLog,
    COSECAttendanceArguments,
)

# Register your models here.
admin.site.register(BiometricDevices)
admin.site.register(BiometricEmployees)
admin.site.register(COSECAttendanceArguments)


@admin.register(BiometricPushLog)
class BiometricPushLogAdmin(admin.ModelAdmin):
    """Records received from push devices, to trace unmatched PINs."""

    list_display = ("punch_time", "device_id", "user_id", "employee_id", "result")
    list_filter = ("result", "device_id")
    search_fields = ("user_id", "message")
    readonly_fields = [field.name for field in BiometricPushLog._meta.fields]
