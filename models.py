from django.db import models


class Global(models.Model):
    roor_dir = models.TextField()
    pkcscmd = models.TextField()
    opensslcmd = models.TextField()
    openssl_key_config_file = models.TextField()

    class Meta:
        db_table = 'global'

class Openssl(models.Model):
    openssl_key_size = models.TextField()
    openssl_ca_key_expire = models.TextField()
    openssl_user_key_expire = models.TextField()
    openssl_key_country = models.TextField()
    openssl_key_province = models.TextField()
    openssl_key_city = models.TextField()
    openssl_key_organization = models.TextField()
    openssl_key_organization_unit = models.TextField()
    openssl_key_master_email = models.TextField()

    class Meta:
        db_table = "openssl"
