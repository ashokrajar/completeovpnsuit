#
# Easy OpenVPN - Complete OpenVPN Suit    
# Copyright (c) 2010 Easy OpenVPN. All rights reserved.
#
# Released under the GPL - see www.gpl.org


# Python Modules
import os
import commands

# django Modules
from django.shortcuts import render_to_response
from django.template import RequestContext
from completeovpnsuit import models

# Custom Modules
# from completeovpnsuit.modules.webmod import render_to_response


# Get Server Daemon User
global server_user
server_user = os.getuid()


# Setup StartUp Screen
def setup_home(request):
    local_vars = {}
    local_vars['setup_step'] = 1
    fd = open(os.path.dirname(os.path.realpath(__file__)) + "/../LICENSE.txt", 'r')
    local_vars['license_data'] = fd.read()
    fd.close()
    return render_to_response('setup.html', local_vars, RequestContext(request))

# Main Setup Function
def eovpn_setup(request):
    local_vars = {}
    local_vars['server_user'] = server_user
    # Check if User is root
    if server_user == 0 :
        # Step 1
        # Accept License
        # /setup/ URL is hit 
        if request.method == 'GET':
            return setup_home(request)
        # Step 2
        elif request.method == 'POST':
            # Continue to Step 2
            # 
            if 'license' in request.POST and request.POST['license'] == 'accept_license':
                local_vars['setup_step'] = 2
                return render_to_response('setup.html', local_vars, RequestContext(request))
            elif 'openssl_config' in request.POST and request.POST['openssl_config'] == 'Configure OpenSSL':
                # Continue to Step 2
                # Validate the Data  
                # user_key_expiry': [u'60'], u'key_province': [u'Tamil Nadu'], u'key_country': [u'IN'], u'key_city': [u'Madurai'], u'master_email': [u'easyovpn@gmail.com'], u'openssl_config': [u'Configure OpenSSL'], u'key_unit': [u'System Engineering'], u'key_size': [u'1024'], u'csrfmiddlewaretoken': [u'dabb9c5dbada6750a915ac69a6cf9829'], u'ca_key_expiry': [u'3650'], u'key_organization': [u'Easy OpenVPN Pvt Ltd'
                local_vars['setup_step'] = 3
                local_vars['post_data'] = request.POST
                return render_to_response('setup.html', local_vars, RequestContext(request))
            else:
                # If the request method is other than GET and POST still show the Setup Home Page
                return setup_home(request)
        else:
            # If the request method is other than GET and POST still show the Setup Home Page
            return setup_home(request)
    else:
        # Display User Error
        local_vars = {}
        local_vars['error'] = "user"
        local_vars['server_user'] = server_user
        return render_to_response('error.html', local_vars, RequestContext(request))


