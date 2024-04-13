from django.contrib import admin
from .models import Doctor, Patient

# Register your models here.
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialization', 'availability', 'hospital', 'phone_number']
    search_fields = ['user__email', 'specialization', 'hospital', 'phone_number']
admin.site.register(Patient)