from django.contrib import admin
from django.db import models
from .models import Patient, Staff, PatientRecord
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.unregister(User)

class CustomUserAdmin(UserAdmin):

    def delete_view(self, request, object_id, extra_context=None):
        if not self.queryset(request).filter(id=object_id).exists():
            return HttpResponseRedirect(reverse('admin:app_Staff_changelist'))
        return super(CustomUserAdmin, self).delete_view(request, object_id, extra_context)
    
    def history_view(self, request, object_id, extra_context=None):
        if not self.queryset(request).filter(id=object_id).exists():
            return HttpResponseRedirect(reverse('admin:app_Staff_changelist'))
        return super(CustomUserAdmin, self).history_view(request, object_id, extra_context)

    
    def queryset(self, request):
        qs = super(CustomUserAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(first_name=request.user)
        
    def save_model(self, request, obj, form, change):
        if change:
            obj.last_name = request.user
            super(CustomUserAdmin, self).save_model(request, obj, form, change)
        else:
            obj.first_name = request.user
            super(CustomUserAdmin, self).save_model(request, obj, form, change)
        
class StaffAdmin(admin.ModelAdmin):
    exclude = ['hospital']
    list_display = ['firstname', 'lastname', 'staff_id']
    list_filter = ['hospital', 'title']
    def change_view(self, request, object_id, form_url = "",extra_context=None):
        if not self.queryset(request).filter(id=object_id).exists():
            return HttpResponseRedirect(reverse('admin:app_Staff_changelist'))
        return super(StaffAdmin, self).change_view(request, object_id, form_url, extra_context) 
    
    def delete_view(self, request, object_id, extra_context=None):
        if not self.queryset(request).filter(id=object_id).exists():
            return HttpResponseRedirect(reverse('admin:app_Staff_changelist'))
        return super(StaffAdmin, self).delete_view(request, object_id, extra_context)
    
    def history_view(self, request, object_id, extra_context=None):
        if not self.queryset(request).filter(id=object_id).exists():
            return HttpResponseRedirect(reverse('admin:app_Staff_changelist'))
        return super(StaffAdmin, self).history_view(request, object_id, extra_context)
    
    def queryset(self, request):
        qs = super(StaffAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(hospital=request.user)
        
    def save_model(self, request, obj, form, change):
        obj.hospital = request.user
        super(StaffAdmin, self).save_model(request, obj, form, change)


class PatientAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname', 'Birthcertificate_no', 'Patientid', 'county', 'added_by']
    list_filter = ['added_by__hospital', 'gender']

class PatientRecordAdmin(admin.ModelAdmin):
    list_display = ['Patientid', 'Birth_certificate_no', 'doctorOnLastVisit']
    list_filter = ['date', 'doctorOnLastVisit__hospital']
    
    def Birth_certificate_no(self, obj):
        return obj.Birthcertificate_no.Birthcertificate_no

admin.site.register(User, CustomUserAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(PatientRecord, PatientRecordAdmin)
