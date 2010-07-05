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
    # Generate Diffie-Hellman parameters for the server side
    # of an SSL/TLS connection.
    if cmd_options.key_type == "dh":
        dh_file = modules.common.server_key_dir + "/dh" + modules.common.openssl_key_size + ".pem"
        if os.path.exists(dh_file):
            sys.stderr.write("Error : Couldn't Create (Diffie-Hellman) Parameters Already Exists.\nOverwriting the Parameters may Break the CompleteOVPNSuit Functionality.\n")
            sys.exit(246)
        else:
            try:
                proc = subprocess.Popen([modules.common.opensslcmd, 'dhparam', '-out', dh_file, modules.common.openssl_key_size], shell=False, bufsize=4096, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except OSError, e:
                sys.stderr.write("Error : Couldn't Create (Diffie-Hellman Parameters")
                sys.exit(246)
            print "Generating Diffie-Hellman parameters, 1024 bit long safe prime, generator 2\nThis is going to take a long time, Please Wait .."
            while proc.poll() == None:
                modules.common.show_rotating_progressmarker()
            print "Completed."
    # Create the Certificate Authority Private Key and Certificate
    elif cmd_options.key_type == "ca":
        if os.path.exists(modules.common.ca_key_file) and os.path.exists(modules.common.ca_cert_file):
            sys.stderr.write("Error : Couldn't Create (CA) Key and Certificate Already Exists.\nOverwriting the CA may Break the CompleteOVPNSuit Functionality.\n")
            sys.exit(245)
        else:
            try:
                proc = subprocess.Popen([modules.common.opensslcmd, 'req', '-batch', '-days', modules.common.openssl_ca_key_expire, '-nodes', '-new', '-newkey', 'rsa:' + modules.common.openssl_key_size, '-sha1', '-x509', '-keyout', modules.common.ca_key_file, '-out', modules.common.ca_cert_file, '-config', modules.common.openssl_key_config_file], shell=False, bufsize=4096, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={"COVPNS_ROOT": modules.common.covpns_root, "KEY_SIZE": modules.common.openssl_key_size, "KEY_COUNTRY": modules.common.openssl_key_country, "KEY_PROVINCE": modules.common.openssl_key_province, "KEY_CITY": modules.common.openssl_key_city, "KEY_ORG": modules.common.openssl_key_organization, "KEY_OU": modules.common.openssl_key_organization_unit, "KEY_CN": modules.common.sys_hostname, "KEY_NAME": modules.common.sys_hostname, "KEY_EMAIL": modules.common.openssl_key_master_email, "PKCS11_MODULE_PATH": "", "PKCS11_PIN": "", "RANDFILE": modules.common.covpns_root + "/keys/.rand", "HOME": modules.common.covpns_root})
            except OSError, e:
                sys.stderr.write("Error : Couldn't Create (CA) Key, Cert")
                sys.exit(245)
            print "Generating CA Key/Cert, Please Wait"
            while proc.poll() == None:
                modules.common.show_rotating_progressmarker()
            os.chmod(modules.common.ca_key_file, 0600)
            fd = open(modules.common.server_key_dir + "/data/index.txt", 'w')
            fd.write('')
            fd.close()
            fd = open(modules.common.server_key_dir + "/data/serial", 'w')
            fd.write('01\n')
            fd.close()
            print "Completed."
    # Create the Server Keys/Certificate
    elif cmd_options.key_type == "server":
        # Check if Server Common Name is Given
        try:
            cmd_args[0]
        except IndexError:
            cmd_parser.error("-c option requires 'Server Common Name' to be Passed with server KEYTYPE")
        # Validate the Common Name
        if modules.common.validate_openssl_commonname(cmd_args[0]) == 1:
            # Check if CA Cert Exists
            if os.path.exists(modules.common.ca_key_file) and os.path.exists(modules.common.ca_cert_file):
                # Check if the Server Cert Already Exists
                if os.path.exists(modules.common.server_key_file) and os.path.exists(modules.common.server_cert_file):
                    sys.stderr.write("Error : Couldn't Create Server Key and Certificate Already Exists.\nOverwriting the Server Certificate may Break the CompleteOVPNSuit Functionality.\n")
                    sys.exit(244)
                else:
                    # Create Key/Certificate and CSR
                    try:
                        proc = subprocess.Popen([modules.common.opensslcmd, 'req', '-batch', '-days', modules.common.openssl_server_key_expire, '-nodes', '-new', '-newkey', 'rsa:' + modules.common.openssl_key_size, '-keyout', modules.common.server_key_file, '-out', modules.common.server_csr_file, '-extensions', 'server', '-config', modules.common.openssl_key_config_file], shell=False, bufsize=4096, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={"COVPNS_ROOT": modules.common.covpns_root, "KEY_SIZE": modules.common.openssl_key_size, "KEY_COUNTRY": modules.common.openssl_key_country, "KEY_PROVINCE": modules.common.openssl_key_province, "KEY_CITY": modules.common.openssl_key_city, "KEY_ORG": modules.common.openssl_key_organization, "KEY_OU": modules.common.openssl_key_organization_unit, "KEY_CN": cmd_args[0], "KEY_NAME": modules.common.sys_hostname, "KEY_EMAIL": modules.common.openssl_key_master_email, "PKCS11_MODULE_PATH": "", "PKCS11_PIN": "", "RANDFILE": modules.common.covpns_root + "/keys/.rand", "HOME": modules.common.covpns_root})
                    except OSError, e:
                        sys.stderr.write("Error : Couldn't Create Server Key, Cert")
                        sys.exit(244)
                    print "Generating Server Key/CSR, Please Wait"
                    while proc.poll() == None:
                        modules.common.show_rotating_progressmarker()
                    os.chmod(modules.common.server_key_file, 0600)
                    # Sign the CSR
                    try:
                        proc = subprocess.Popen([modules.common.opensslcmd, 'ca', '-batch', '-days', modules.common.openssl_server_key_expire, '-out', modules.common.server_cert_file, '-in', modules.common.server_csr_file, '-extensions', 'server', '-md', 'sha1', '-config', modules.common.openssl_key_config_file], shell=False, bufsize=4096, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={"COVPNS_ROOT": modules.common.covpns_root, "KEY_SIZE": modules.common.openssl_key_size, "KEY_COUNTRY": modules.common.openssl_key_country, "KEY_PROVINCE": modules.common.openssl_key_province, "KEY_CITY": modules.common.openssl_key_city, "KEY_ORG": modules.common.openssl_key_organization, "KEY_OU": modules.common.openssl_key_organization_unit, "KEY_CN": modules.common.sys_hostname, "KEY_NAME": modules.common.sys_hostname, "KEY_EMAIL": modules.common.openssl_key_master_email, "PKCS11_MODULE_PATH": "", "PKCS11_PIN": "", "RANDFILE": modules.common.covpns_root + "/keys/.rand", "HOME": modules.common.covpns_root})
                    except OSError, e:
                        sys.stderr.write("Error : Couldn't Sign Server CSR")
                        sys.exit(244)
                    print "Signing Server CSR, Please Wait"
                    while proc.poll() == None:
                        modules.common.show_rotating_progressmarker()
                    print "Completed."
            else:
                sys.stderr.write("Error : Couldn't find CA Certificate for creating Server Key/Cert.\nFirst Run covpns-manage.py -c ca\n")
        else:
            print "Error : Invalid Common Name '" + cmd_args[0] + "', Only Character, UnderScore and Dot is allowed."
    elif cmd_options.key_type == "user":
        if cmd_options.user_name:
            print "Create User Keys"
            # export CA_EXPIRE KEY_EXPIRE KEY_OU KEY_NAME KEY_CN PKCS11_MODULE_PATH PKCS11_PIN
            sys.exit(1)
        else:
            cmd_parser.error("-c requires an mandatory option -u to be parsed")
    else:
        cmd_parser.error("Invalid Key Type '" + key_type + "',\tValid Key Types : dh, ca, server or user")


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
cmd_parser.add_option("-c", "--create", action="store", type="string", dest="key_type", help="Type of key to be Created : dh, ca, server or user", metavar="KEYTYPE")
cmd_parser.add_option("-u", "--user", action="store", type="string", dest="user_name", help="New/Existing VPN UserName", metavar="USER")
(cmd_options, cmd_args) = cmd_parser.parse_args()


# Validate the User Input Data
# List Users
if cmd_options.list_user:
    print "List Users"
    sys.exit(0)
# Create Keys
if cmd_options.key_type:
    create_key(cmd_options.key_type)
# If none match, Exit with help
else:
    cmd_parser.print_help()
    sys.exit(1)

# Create Appropriate Keys
