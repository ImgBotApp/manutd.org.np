# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-03 10:23
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import froala_editor.fields
import muscn.utils.location


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', froala_editor.fields.FroalaField(blank=True, null=True)),
                ('email', django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(blank=True, max_length=254, null=True), size=None)),
                ('phone', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), size=None)),
                ('fax', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), size=None)),
                ('facebook_page', models.URLField(blank=True, null=True)),
                ('facebook_group', models.URLField(blank=True, null=True)),
                ('twitter', models.URLField(blank=True, null=True)),
                ('instagram', models.URLField(blank=True, null=True)),
                ('google_plus', models.URLField(blank=True, null=True)),
                ('linkedin', models.URLField(blank=True, null=True)),
                ('github', models.URLField(blank=True, null=True)),
                ('location', muscn.utils.location.LocationField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(max_length=255)),
                ('message', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
