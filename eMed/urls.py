from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url('^$', 'app.views.staffLogin'),
                       url('^logout', 'app.views.staffLogout'),
                       url('^password_change', 'django.contrib.auth.views.password_change'),
                       url('^profile/search', 'app.views.patientSearch'),
                       url('^profile/PatientAdd', 'app.views.addPatient'),
                       url('^profile/update', 'app.views.editPatient'),
                       url('^updateRecord', 'app.views.updateRecord'),
                       url('^medicalHistory', 'app.views.medicalHistory'),
                       url(r'^medicalDetails/(?P<pk>\d+)/$', 'app.views.medicalDetails'),
                       
                       
                       
    # Examples:
    # url(r'^$', 'MedicalRecords.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
)
