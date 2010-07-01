#! /usr/bin/python -d
# Copyright (c) 2010 Skynet Pvt Ltd. All rights reserved.
# Released under the GPL - see www.gpl.org

'''Global Variable and Common Function declaration for Complete OVPN Suit.

Author      :       Ashok Raja R <ashokraja.linux@gmail.com>
Project     :       Complete OVPN Suit
'''


# Initialize the Settings Database
db_conn = sqlite3.connect(covpns_install_dir + "/data/settings.db")
settings_db = db_conn.cursor()

# Close Database
settings_db.close()

# Function to get the User Confirmation
def get_user_confirmation(user_message,continue_program):
    '''get_user_confirmation('User Defined Message to be Display','continue/no')'''

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