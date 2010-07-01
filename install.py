#! /usr/bin/python -d
# Copyright (c) 2010 Skynet Pvt Ltd. All rights reserved.
# Released under the GPL - see www.gpl.org

'''
This program installs the Complete OVPN Suit under the installation Path.
It also does the initial configuration required for running Complete OVPN Suit.

Usage :
```````
shell> sudo python install.py

Author      :       Ashok Raja R <ashokraja.linux@gmail.com>
Project     :       Complete OVPN Suit
Dependency  :       OS - Ubuntu 8.04
                    Language - Python 2.5
'''


#-----------------------|
# Import Python Modules |
#-----------------------|
import os
import sys
import tarfile
import commands
import re
import shutil
import datetime
import sqlite3


#----------------|
# Global objects |
#----------------|
# Date object
date = datetime.datetime.now()


#--------------------|
# Global Identifiers |
#--------------------|
# Set Installer Directory
covpns_installer_dir = os.getcwd()



#-----------------------|
# Function declarations |
#-----------------------|
# Function to get the User Confirmation
def get_user_confirmation(user_message,continue_program):
    '''get_user_confirmation('User Defined Message to be Display','continue/no')
    Display the User Defined Message and prompts for confimation, User should Confirm with 'yes' or 'no'.
    When user confirms with enter as input, it is considered yes.
    '''
    try:
        user_confirms = raw_input(user_message  + ' [yes] : ')
    except KeyboardInterrupt:
        print "\nUser Terminated"
        raise sys.exit(254)
    except EOFError:
        get_user_confirmation("\n" + user_message,continue_program)
    else:
        # Input Data Validation
        if len(user_confirms) == 0:
            return 0
        elif user_confirms.lower() != 'yes':
            if user_confirms.lower() == 'no':
                if continue_program != 'continue':
                    raise sys.exit(254)
                else:
                    return 0
            else:
                get_user_confirmation(user_message,continue_program)

# Function to get User Input
def get_user_input(user_message):
    '''get_user_input('User Defined Message to be Display')
    Display the User Defined Message and prompts for User Data.'''
    try:
        user_data = raw_input(user_message)
    except KeyboardInterrupt:
        print "\nUser Terminated"
        raise sys.exit(254)
    except EOFError:
        get_user_input("\n" + user_message)
    else:
        return user_data

# Function to Validate Key Data Input
def validate_openssl_keydata(openssl_keydata):
    '''validate_openssl_keydata('data')
    Returns True if the Data Matches the Regular Expression '^[a-zA-Z\s]{1,}$' '''
    # Regular Expression for Matching
    pattern = re.compile('^[a-zA-Z\s]{1,}$')
    if pattern.search(openssl_keydata):
        return_value  = pattern.search(openssl_keydata).group()
        return True
    else:
        return False

# Function to Validate E-Mail Address
def validate_email_addr(email_addr):
    '''validate_email_addr('E-Mail')
    Returns True if it is a Valid E-Mail Address'''
    # Regular Expression for Matching
    pattern = re.compile("[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?")
    if pattern.search(email_addr):
        return_value  = pattern.search(email_addr).group()
        return True
    else:
        return False

# Function for Post Installation #
def post_install():
    '''Runs the Complete OVPN Suit Post Installation.'''
    # Global Settings
    print "\nConfiguring Complete OVPN Suit :\n```````````````````````````````"
    print "Complete OVPN Suit is Installed but not yet configured, Running first run Configuration\n"
    print "Configuring Complete OVPN Suit ROOT Path : " + covpns_install_dir
    print "Configuring pkcs11tool Command PATH to " + pkcs11toolcmd
    # Openssl Config
    print "\nConfiguring OpenSSL Key Properties"
    # Get the Information from user,validate and update in configuration
    print "Configuring OpenSSL Command PATH to " + opensslcmd
    openssl_key_config_file = covpns_install_dir + "/conf/openssl.cnf"
    print "Using OpenSSL Key Configuration file in : " + openssl_key_config_file
    # Get the key Size
    openssl_key_size = get_user_input("Enter the OpenSSL key size [1024] : ")
    if len(openssl_key_size) == 0:
        openssl_key_size = "1024"
    elif openssl_key_size.isdigit():
        if int(openssl_key_size) != 1024:
            if int(openssl_key_size) == 2048:
                print "warning : Using key size as 2048 will slow down TLS negotiation.\n"
            else:
                print "Note: key size you entered couldn't be used, Using default key size 1024.\n"
                openssl_key_size = "1024"
    else:
        print "Note : key size Days you entered is not valid, using default key size 1024\n"
        openssl_key_size = "1024"
    # Get the CA Key expiry
    openssl_ca_key_expire = get_user_input("Enter the OpenSSL CA Certificate Expiry Days [3650] : ")
    if len(openssl_ca_key_expire) == 0:
        openssl_ca_key_expire = "3650"
    elif openssl_ca_key_expire.isdigit():
        if int(openssl_ca_key_expire) > 0:
            if int(openssl_ca_key_expire) < 365:
                print "Note : Recommended CA certificate Expiry Days shoud be atleast 365, using default days 3650\n"
                openssl_ca_key_expire = "3650"
        else:
            print "Note : CA certificate Expiry Days can't be a negative value, using default days 3650\n"
            openssl_ca_key_expire = "3650"
    else:
        print "Note : CA certificate Expiry Days you entered is not valid, using default days 3650\n"
        openssl_ca_key_expire = "3650"
    # Get Key Country
    openssl_key_country = get_user_input("Enter Key Country [IN] : ")
    if int(openssl_key_country.isalpha()) != 1 or len(openssl_key_country) != 2:
        print "Warning : Invalid Country Code '" + openssl_key_country + "'.No Special Characters, Numbers are allowed and only Two Characters is allowed. eg: IN.\nUsing default Country 'IN'"
        openssl_key_country = "IN"
    # Get Key Province/State
    openssl_key_province = get_user_input("Enter Key Province/State [Tamil Nadu] : ")
    if validate_openssl_keydata(openssl_key_province) != 1:
        print "Warning : Invalid Province/State '" + openssl_key_province + "' Only Characters are allowed, Using default Province 'Tamil Nadu'"
        openssl_key_province = "Tamil Nadu"
    # Get Key City
    openssl_key_city = get_user_input("Enter Key City [Madurai] : ")
    if validate_openssl_keydata(openssl_key_city) != 1:
        print "Warning : Invalid City '" + openssl_key_city + "' Only Characters are allowed, Using default City 'Madurai'"
        openssl_key_province = "Madurai"
    # Get Key Organization
    openssl_key_organization = get_user_input("Enter Key Organiazation Name [MyCompany Pvt Ltd] : ")
    if validate_openssl_keydata(openssl_key_organization) != 1:
        print "Warning : Invalid City '" + openssl_key_organization + "' Only Characters are allowed, Using default Organization 'MyCompany Pvt Ltd'"
        openssl_key_organization = "MyCompany Pvt Ltd"
    # Get Key Master E-Mail
    openssl_key_master_email = get_user_input("Enter Company E-Mail [xyz@mycompany.com] : ")
    if validate_openssl_keydata(openssl_key_master_email) != 1:
        print "Warning : Invalid Email '" + openssl_key_master_email + "', Using default xyz@mycompany.com"
    # Get the User Key expiry
    openssl_user_key_expire = get_user_input("Enter the User Certificate Expiry Days [30] : ")
    if len(openssl_user_key_expire) == 0:
        openssl_user_key_expire ="30"
    elif openssl_user_key_expire.isdigit():
        if int(openssl_user_key_expire) > 0:
            if int(openssl_user_key_expire) < 30:
                print "Warning : Recommended User certificate Expiry Days shoud be atleast 30.\n"
                openssl_user_key_expire ="30"
            elif int(openssl_user_key_expire) > 90:
                get_user_confirmation('Alert : Setting User Certificate Expiry more than 90 Days is a Security Risk.','continue')
        else:
            print "Note : User certificate Expiry Days can't be a negative value, using default days 30\n"
            openssl_user_key_expire ="30"
    else:
        print "Note : User certificate Expiry Days you entered is not valid, using default days 30\n"
        openssl_user_key_expire ="30"
    # Initialize the Settings Database
    db_conn = sqlite3.connect(covpns_install_dir + "/data/settings.db")
    settings_db = db_conn.cursor()
    # Create/Insert/Update Global Settings Table
    settings_db.execute('''create table global (root_dir text, pkcscmd text)''')
    settings_db.execute('insert into global values (?,?)',(covpns_install_dir,pkcs11toolcmd))
    # Create/Insert/Update Openssl Settings Table
    settings_db.execute('''create table openssl (opensslcmd text,openssl_key_config_file text,openssl_key_size text,openssl_ca_key_expire text,openssl_user_key_expire text,openssl_key_country text,openssl_key_province tex,openssl_key_city text,openssl_key_organization text,openssl_key_master_email text)''')
    settings_db.execute('insert into openssl values (?,?,?,?,?,?,?,?,?,?)',(opensslcmd,openssl_key_config_file,openssl_key_size,openssl_ca_key_expire,openssl_user_key_expire,openssl_key_country,openssl_key_province,openssl_key_city,openssl_key_organization,openssl_key_master_email))
    # Save the Changes to Database
    db_conn.commit()
    # Close Database
    settings_db.close()
    # Finally Exit
    raise sys.exit(0)

# Function to do clean up of Directories
def clean_up(install_path):
    '''clean_up('path')
    Removes the leaf directory and all empty sub-directries'''
    os.removedirs(install_path)

#--------------------------|
# Main Program Starts Here |
#--------------------------|

#-- Check if User is root --#
if os.getuid() != 0:
    print "ERROR : Current User Doesn't seems to have Sufficient Previledge.\n"
    print "This script requires ROOT Previlege for the Installation and Administrative Actions."
    print "Most of the time it can be accomplised by executing\nshell> sudo python install.py\n"
    raise sys.exit(255)

# Clear the Screen
os.system('clear')

#-- Start the Installation --#
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n| Complete OVPN Suit Installation |\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"

# Check for all the Dependencies
print "Pre-Requistics Check :\n``````````````````````"
# Check for openssl
print "Checking for OpenSSL\t\t:\t",
sslcmd_status = commands.getstatusoutput("which openssl")
if sslcmd_status[0] == 0:
    opensslcmd = sslcmd_status[1]
    print "Installed"
elif sslcmd_status[0] == 256:
    print "Not Found\nError : openssl command not found in $PATH\nEither OpenSSL not-installed or installed on different Location."
    print "If openssl is installed make sure it exists in the OS standard $PATH."
    print "If openssl is not installed, You can install it by typing:\nsudo apt-get install openssl"
    raise sys.exit(248)
else:
    print "Not Found\nError : " +  sslcmd_status[1] + "\nEither OpenSSL not-installed or installed on different Location."
    raise sys.exit(248)
# Check for pkcs11-tool
print "Checking for pkcs11-tool\t:\t",
sslcmd_status = commands.getstatusoutput("which pkcs11-tool")
if sslcmd_status[0] == 0:
    pkcs11toolcmd = sslcmd_status[1]
    print "Installed"
elif sslcmd_status[0] == 256:
    print "Not Found\nError : pkcs11-tool command not found in $PATH\nEither opensc not-installed or installed on different Location."
    print "If opensc is installed make sure it exists in the OS standard $PATH."
    print "If opensc is not installed, You can install it by typing:\nsudo apt-get install opensc "
    raise sys.exit(247)
else:
    print "Not Found\nError : " +  sslcmd_status[1] + "\nEither opensc not-installed or installed on different Location."
    raise sys.exit(247)


# Get the Installation Directory from User
user_install_dir = get_user_input("\nWhere do you want 'Complete OVPN Suit' to be Installed [/opt/] : ")
if len(user_install_dir) == 0:
    covpns_install_dir = r"/opt/completeovpnsuit"
else:
    user_install_dir = r"/" + user_install_dir + r"/completeovpnsuit"
    covpns_install_dir = os.path.abspath(user_install_dir)
# Check if the Installation Directory already Exists.
# If it exists run the post install after getting user confirmation
if os.path.exists(covpns_install_dir):
    print "\nError : " + covpns_install_dir + " already Exists. Looks like some other version of Complete OVPN Suit is installed."
    get_user_confirmation('Do you want to Re-Configure Complete OVPN Suit by Running the Post-Install Script ? ','no')
    if os.path.exists(covpns_install_dir + "/data/settings.db"):
        get_user_confirmation('Warning : This will overwrite the existing Configuration. Still you want to Continue ? ','no')
        backup_file = covpns_install_dir + "/backup/settings.db_backup_"+date.strftime("%d-%m-%Y_%H-%M")
        shutil.move(covpns_install_dir + "/data/settings.db",backup_file)
        print "\nNote : Old Configuration backuped in "+ backup_file
    post_install()
# Get Users Confirmation and Continue with the Installation
get_user_confirmation('Complete OVPN Suit will be Installed in [' + covpns_install_dir + "]. Can I Continue ?", 'no')


#-- Start to Install OpenVPN --#
# Extract the openvpn package
print "\n\nInstalling OpenVPN-2.1.1 :\n``````````````````````````"
print "Extracting openvpn-src.tgz to /usr/local/src/openvpn-src"
openvpn_tgz = tarfile.open(covpns_installer_dir + "/src/openvpn-src.tgz")
openvpn_tgz.extractall(path=r"/usr/local/src/")
openvpn_tgz.close()

# configure/Make/make
# Run configure
print "Running ./configure"
os.chdir("/usr/local/src/openvpn-src")
config_status = commands.getstatusoutput("sudo ./configure")
# If ./configure failed Fetch the error to display
if config_status[0] != 0:
    pattern = re.compile('(.*?)configure(.*?)error.*',re.M)
    error_report = pattern.search(config_status[1]).group()
    print "Error [" + str(config_status[0]) + "] : " + error_report
    # Generate Error Report if Possible
    if config_status[0] == 256:
        if "error: no acceptable C compiler found" in error_report:
            print "\nLooks like gcc package is  not installed. You can install it by typing:\nsudo apt-get install gcc libc6-dev"
            sys.exit(253)
        elif "error: Or try ./configure --disable-lzo" in error_report:
            print "\nLooks like liblzo-dev package is  not installed. You can install it by typing:\nsudo apt-get install liblzo-dev"
            sys.exit(253)
        elif "error: OpenSSL Crypto headers not found" in error_report:
            print "\nLooks like libssl-dev package is  not installed. You can install it by typing:\nsudo apt-get install libssl-dev"
            sys.exit(253)
        else:
            sys.exit(253)
    elif config_status[0] == 19712:
        print "\nLooks like libc6-dev package is  not installed. You can install it by typing:\nsudo apt-get install libc6-dev"
        sys.exit(253)
    else:
        sys.exit(253)

# Run make
print "Running make"
make_status = commands.getstatusoutput("sudo make")
# If make failed, Fetch the error to display
if make_status[0] != 0:
    error_report = make_status[1]
    print "Error [" + str(make_status[0]) + "] : " + error_report
    # Generate Error Report if Possible
    if make_status[0] == 256:
        print "\nLooks like make package is  not installed. You can install it by typing:\nsudo apt-get install make"
        sys.exit(250)
    else:
        sys.exit(250)

# Run make install
print "Running make install"
make_install_status = commands.getstatusoutput("sudo make install")
# If make install failed, Fetch the error to display
if make_install_status[0] != 0:
    error_report = make_install_status[1]
    print "Error [" + str(make_install_status[0]) + "] : " + error_report
    # Generate Error Report if Possible
    if make_install_status[0] == 256:
        print "\nLooks like make package is  not installed. You can install it by typing:\nsudo apt-get install make"
        sys.exit(250)
    else:
        sys.exit(250)

#-- Install Complete OVPN Suit --#
print "\nInstalling Complete OVPN Suit :\n```````````````````````````````"
print "Creating required files and directories"
os.makedirs(covpns_install_dir)
os.makedirs(covpns_install_dir + "/data", mode=0700)
os.makedirs(covpns_install_dir + "/user-keys", mode=0700)
os.makedirs(covpns_install_dir + "/keys/ca", mode=0700)
os.makedirs(covpns_install_dir + "/keys/certs", mode=0700)
os.makedirs(covpns_install_dir + "/keys/crl", mode=0700)
os.makedirs(covpns_install_dir + "/keys/database", mode=0700)
os.makedirs(covpns_install_dir + "/tmp", mode=1770)
os.makedirs(covpns_install_dir + "/pid", mode=0700)
os.makedirs(covpns_install_dir + "/backup", mode=0755)
print "Copying files and directories from Installer to Installation Path"
shutil.copytree(covpns_installer_dir + "/bin",covpns_install_dir + "/bin")
shutil.copytree(covpns_installer_dir + "/conf",covpns_install_dir + "/conf")
shutil.copytree(covpns_installer_dir + "/doc",covpns_install_dir + "/doc")
shutil.copytree(covpns_installer_dir + "/htdocs",covpns_install_dir + "/htdocs")

#-- First Run --#
post_install()