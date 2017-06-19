# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Articles(models.Model):
    article_link = models.TextField()
    article_content = models.TextField(null=True)
    article_title = models.CharField(max_length=255, null=True)
    article_content_summary = models.TextField(null=True)
    article_title_summary = models.CharField(max_length=255, null=True)
    published_date = models.DateTimeField('date published', null=True)