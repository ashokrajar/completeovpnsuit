#! /usr/bin/python -d
#
# Easy OpenVPN - Complete OpenVPN Suit    
# Copyright (c) 2010 Easy OpenVPN. All rights reserved.
#
# Released under the GPL - see www.gpl.org

'''Global Identifier and Customs Function declaration for Complete OVPN Suit.

Author      :       Ashok Raja R <ashokraja.linux@gmail.com>
Project     :       Easy OpenVPN
'''

from django.shortcuts import render_to_response
from django.template import RequestContext


# This is a Wrapper function to django render_to_response
def render_to_response(request, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(request)
    return render_to_response(*args, **kwargs)
