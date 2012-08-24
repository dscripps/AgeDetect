from django.conf.urls import patterns, include, url

from age_detect import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^upload/$', 'age_detect_app.views.upload_file'),
    url(r'^test_svms/$', 'age_detect_app.views.test_svms'),
    # url(r'^$', 'age_detect.views.home', name='home'),
    # url(r'^age_detect/', include('age_detect.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': "{0}uploads".format(settings.MEDIA_ROOT),
    })
)