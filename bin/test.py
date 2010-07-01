#! /usr/bin/python -d
# Copyright (c) 2010 Skynet Pvt Ltd. All rights reserved.

'''
Author      :       Ashok Raja R <ashokraja.linux@gmail.com>
Project     :       Complete OVPN Suit
'''
import subprocess
import os
import sys
import time

p = subprocess.Popen("mytest", shell=True, bufsize=4096, stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)

print "Please Wait, While we Create the Key ...."
while p.poll() == None:
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

#pbar.finish()
print p.communicate()

#p.communicate("q")
