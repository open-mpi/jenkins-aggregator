# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pullID', models.IntegerField()),
                ('sha', models.CharField(max_length=200)),
                ('triggerTime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ResultSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sourceID', models.CharField(max_length=200)),
                ('timeReceived', models.DateTimeField()),
                ('passed', models.BooleanField()),
                ('rawResults', models.FileField(upload_to=b'')),
                ('commit', models.ForeignKey(to='aggregator.Commit')),
            ],
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('passed', models.BooleanField()),
                ('skipped', models.BooleanField()),
                ('description', models.CharField(max_length=200)),
                ('output', models.CharField(max_length=200)),
                ('resultSet', models.ForeignKey(to='aggregator.ResultSet')),
            ],
        ),
    ]
