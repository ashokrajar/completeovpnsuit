#
# Easy OpenVPN - Complete OpenVPN Suit    
# Copyright (c) 2010 Easy OpenVPN. All rights reserved.
#
# Released under the GPL - see www.gpl.org

from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

from completeovpnsuit.views import *
from completeovpnsuit.setup.views import *

# Admin Module
admin.autodiscover()

# URL Configuration
urlpatterns = patterns('',
                       (r'^admin/', include(admin.site.urls)),
                       (r'^$', covpns_home_page),
                       (r'^setup/$', eovpn_setup),
                       (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
