#! /usr/bin/python -d
# Copyright (c) 2010 Skynet Pvt Ltd. All rights reserved.

'''
Author      :       Ashok Raja R <ashokraja.linux@gmail.com>
Project     :       Complete OVPN Suit
'''


#-----------------------|
# Import Python Modules |
#-----------------------|
import os
import sys
import subprocess
from optparse import OptionParser

# Import Custom Modules
import modules.common


#-----------------------|
# Function declarations |
#-----------------------|
# Function for Creating the Keys
def create_key(key_type):
    # Build Diffie-Hellman parameters for the server side
    # of an SSL/TLS connection.
    if cmd_options.key_type == "dh":
        print "Creating dh .."
        dhparam_cmd = modules.common.opensslcmd + " dhparam -out " + modules.common.server_key_dir + "/dh" + modules.common.openssl_key_size + ".pem " + modules.common.openssl_key_size
        print dhparam_cmd
        proc = subprocess.Popen(dhparam_cmd, shell=False, bufsize=4096, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        while proc.poll() == None:
            modules.common.show_rotating_progressmarker()

        #if dhparam_status[0] != 0:
        #    print "Error Occured"
        #    print dhparam_status[1]
        #OPENSSL dhparam -out ${KEY_DIR}/dh${KEY_SIZE}.pem ${KEY_SIZE}
        #print "Creating dh"
    elif cmd_options.key_type == "ca":
        print "Creating ca"
    elif cmd_options.key_type == "user":
        if cmd_options.user_name:
            print "Create User Keys"
            sys.exit(1)
        else:
            cmd_parser.error("-c requires an mandatory option -u to be parsed")
    else:
        cmd_parser.error("Invalid Key Type '" + key_type + "',\tValid Key Types : dh, ca or user")


#--------------------------|
# Main Program Starts Here |
#--------------------------|

#-- Check if User is root --#
if os.getuid() != 0:
    print "ERROR : Current User Doesn't seems to have Sufficient Previledge.\n"
    print "This script requires ROOT Previlege for the Installation and Administrative Actions."
    print "Most of the time it can be accomplised by executing\nshell> sudo python install.py\n"
    raise sys.exit(255)

# Initialize covpns Global Variables
modules.common.set_globalvar()

# Command Line Arguments Parser
cmd_parser = OptionParser(version="%prog 1.0")
cmd_parser.add_option("-l", "--list", action="store_true", dest="list_user", help="List the Current User Details")
cmd_parser.add_option("-c", "--create", action="store", type="string", dest="key_type", default="user", help="Type of key to be Created : dh, ca or user    [default: %default]", metavar="KEYTYPE")
cmd_parser.add_option("-u", "--user", action="store", type="string", dest="user_name", help="New/Existing VPN UserName", metavar="USER")
(cmd_options, cmd_args) = cmd_parser.parse_args()

# Validate the User Input Data
# List Users
if cmd_options.list_user:
    print "Users"
    sys.exit(0)
# Create Keys
if cmd_options.key_type:
    create_key(cmd_options.key_type)
# If none match, Exit with help
else:
    cmd_parser.print_help()
    sys.exit(1)

# Create Appropriate Keys
