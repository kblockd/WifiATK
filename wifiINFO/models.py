# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Nativelog(models.Model):
    client = models.CharField(db_column='Client', max_length=17, blank=True, null=True)  # Field name made lowercase.
    bssid = models.CharField(db_column='Bssid', max_length=17, blank=True, null=True)  # Field name made lowercase.
    essid = models.CharField(db_column='Essid', max_length=40, blank=True, null=True)  # Field name made lowercase.
    first_time = models.DateTimeField(db_column='First_time', blank=True, null=True)  # Field name made lowercase.
    last_time = models.DateTimeField(db_column='Last_time', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'nativeLog'


class Stationlog(models.Model):
    client = models.CharField(db_column='Client', max_length=17, blank=True, null=True)  # Field name made lowercase.
    bssid = models.CharField(db_column='Bssid', max_length=17, blank=True, null=True)  # Field name made lowercase.
    essid = models.CharField(db_column='Essid', max_length=8000, blank=True, null=True)  # Field name made lowercase.
    first_time = models.DateTimeField(db_column='First_time', blank=True, null=True)  # Field name made lowercase.
    last_time = models.DateTimeField(db_column='Last_time', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'stationLog'
        unique_together = (('client', 'bssid', 'essid'), ('client', 'bssid'),)


class Wifilog(models.Model):
    bssid = models.CharField(db_column='Bssid', unique=True, max_length=255)  # Field name made lowercase.
    essid = models.CharField(db_column='Essid', max_length=30, blank=True, null=True)  # Field name made lowercase.
    channel = models.IntegerField(db_column='Channel')  # Field name made lowercase.
    privacy = models.CharField(db_column='Privacy', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cipher = models.CharField(db_column='Cipher', max_length=10, blank=True, null=True)  # Field name made lowercase.
    authentication = models.CharField(db_column='Authentication', max_length=10, blank=True, null=True)  # Field name made lowercase.
    first_time = models.DateTimeField(db_column='First_time')  # Field name made lowercase.
    last_time = models.DateTimeField(db_column='Last_time')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'wifiLog'
        unique_together = (('bssid', 'essid'),)
