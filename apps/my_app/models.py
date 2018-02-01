# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length = 100)
    alias = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 255)
    date_of_birth = models.DateField(auto_now=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Quotes(models.Model):
    author = models.CharField(max_length = 100)
    quote = models.CharField(max_length = 255)
    uploaded_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name="uploads")
    favorites = models.ManyToManyField(User, related_name="quote_favorited")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)