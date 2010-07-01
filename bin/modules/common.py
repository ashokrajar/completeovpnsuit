#! /usr/bin/python -d
# Copyright (c) 2010 Skynet Pvt Ltd. All rights reserved.
# Released under the GPL - see www.gpl.org

'''Global Identifier and Customs Function declaration for Complete OVPN Suit.

Author      :       Ashok Raja R <ashokraja.linux@gmail.com>
Project     :       Complete OVPN Suit
'''

import os
import sys
import sqlite3
import time


# Function to Define Global Setings
def set_globalvar():
    '''Initialize global Variables Specific to covpns.
    Variable List :
    covpns_root, pkcs11toolcmd, server_key_dir, user_key_dir, data_dir, pid_dir,
    config_dir, webroot, backup_dir, tmp_dir, openssl_data, opensslcmd,
    openssl_key_config_file, openssl_key_size, openssl_ca_key_expire, openssl_user_key_expire'''
    # Define Global Variables
    global covpns_root, pkcs11toolcmd, server_key_dir, user_key_dir, data_dir, pid_dir, config_dir, webroot, backup_dir, tmp_dir, openssl_data, opensslcmd, openssl_key_config_file, openssl_key_size, openssl_ca_key_expire, openssl_user_key_expire
    # Initialize the Settings Database
    database_dir = os.path.abspath( os.path.abspath(os.path.dirname(sys.argv[0])) + '/../') + "/data/"
    db_conn = sqlite3.connect(database_dir + "settings.db")
    settings_db = db_conn.cursor()

    # Get Data from DB and Configure the Global Variable
    settings_db.execute('select * from global')
    global_data = settings_db.fetchone()
    covpns_root = global_data[0]
    pkcs11toolcmd = global_data[1]
    server_key_dir = covpns_root + "/keys"
    user_key_dir = covpns_root + "/user-keys"
    data_dir = covpns_root + "/data"
    pid_dir = covpns_root + "/pid"
    config_dir = covpns_root + "/conf"
    webroot = covpns_root + "/htdocs"
    backup_dir = covpns_root + "/backup"
    tmp_dir = covpns_root + "/tmp"
    # Get Data from DB and Configure the OpenSSL Variable
    settings_db.execute('select * from openssl')
    openssl_data = settings_db.fetchone()
    opensslcmd = openssl_data[0]
    openssl_key_config_file = openssl_data[1]
    openssl_key_size = openssl_data[2]
    openssl_ca_key_expire = openssl_data[3]
    openssl_user_key_expire = openssl_data[4]

    # Close Database
    settings_db.close()

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

# Function to Display Rotating ProgressMarker
def show_rotating_progressmarker():
    '''Displays a Rotating Progress Marker'''
    for I in range(100):
        sys.stdout.write("(|)\r")
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write("(/)\r")
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write("(-)\r")
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write("(\\)\r")
        sys.stdout.flush()
        time.sleep(0.1)
