# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page', models.CharField(max_length=2000)),
                ('referrer', models.CharField(max_length=2000)),
                ('user_agent', models.CharField(max_length=2000)),
                ('comment', models.CharField(max_length=2000, null=True)),
                ('html', models.TextField(null=True)),
                ('image', models.ImageField(null=True, upload_to=b'duat_feedback')),
                ('created_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-created_date',),
                'permissions': (('readonly_feedback', 'Readonly Feedback'),),
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('notify_admin', models.BooleanField(default=False)),
                ('admin', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='feedback',
            name='project',
            field=models.ForeignKey(to='duat.Project'),
        ),
    ]
