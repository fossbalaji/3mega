# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Sites(models.Model):
    name = models.CharField(null=False, blank=False, max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now_add=True)


class SitesValues(models.Model):
    site_id = models.IntegerField(null=False, blank=False)
    a_value = models.FloatField(default=0.0)
    b_value = models.FloatField(default=0.0)
    created_on = models.DateField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now_add=True)