#
# Easy OpenVPN - Complete OpenVPN Suit    
# Copyright (c) 2010 Easy OpenVPN. All rights reserved.
#
# Released under the GPL - see www.gpl.org


import os
from django.shortcuts import render_to_response
from django.template import RequestContext


import completeovpnsuit.bin.modules.common


# Initialize covpns Global Variables
# completeovpnsuit.bin.modules.common.set_globalvar(database_dir=os.path.dirname(os.path.realpath(__file__)) + "/data/")

def covpns_home_page(request):
    if os.getuid() == 0:
        return render_to_response('common.html')
    else:
        return render_to_response('common.html', locals())

def covpns_login(request):
    return render_to_response('login.html')

