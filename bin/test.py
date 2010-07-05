#! /usr/bin/python -d
# Copyright (c) 2010 Skynet Pvt Ltd. All rights reserved.

'''
Author      :       Ashok Raja R <ashokraja.linux@gmail.com>
Project     :       Complete OVPN Suit
'''

import subprocess
import modules.common

modules.common.set_globalvar()

try:
    proc = subprocess.Popen([modules.common.opensslcmd, 'req', '-batch', '-days', modules.common.openssl_ca_key_expire, '-nodes', '-new', '-newkey', 'rsa:' + modules.common.openssl_key_size, '-sha1', '-x509', '-keyout', '/tmp/ca.key', '-out', '/tmp/ca.crt', '-config', modules.common.openssl_key_config_file], shell=False, bufsize=4096, env={"COVPNS_ROOT": modules.common.covpns_root, "KEY_COUNTRY": modules.common.openssl_key_country, "KEY_PROVINCE": modules.common.openssl_key_province, "KEY_CITY": modules.common.openssl_key_city, "KEY_ORG": modules.common.openssl_key_organization, "KEY_OU": modules.common.openssl_key_organization_unit, "KEY_CN": modules.common.sys_hostname, "KEY_NAME": modules.common.sys_hostname, "KEY_EMAIL": modules.common.openssl_key_master_email})
except OSError, e:
    print e


