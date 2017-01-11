# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-11 10:07
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_name', models.CharField(help_text='Unique Name For Schedule', max_length=100, unique=True)),
                ('schedule_command', models.CharField(help_text='Provide Your command to be run, it can be a full path to bat file', max_length=251, verbose_name='Schedule Command')),
                ('schedule_start', models.DateTimeField(blank=True, default=datetime.datetime(2017, 1, 11, 12, 37, 29, 124004), help_text='Time 24 hours Format', verbose_name='Start Time')),
                ('schedule_option_repeat', models.BooleanField(default=False, help_text='Do you want to Repeat Task on Some Interval?', verbose_name='Repeat Task')),
                ('schedule_option_task_interval', models.IntegerField(blank=True, help_text='Task Interval if Applicable in Minutes (1 - 599940)', null=True, verbose_name='Repeat Task Every')),
                ('schedule_option_duration', models.CharField(blank=True, default='NA', help_text='Task Duraton to be run in HH:MM format, you can mention 120:00 as well for 5 days, indefinite Option Not provided for security purpose', max_length=10, null=True, verbose_name='For a Duration Of')),
                ('schedule_option_recur', models.IntegerField(blank=True, default=1, help_text='Specify Recurrence', null=True, verbose_name='Recur Every')),
                ('schedule_end', models.DateTimeField(blank=True, help_text='Only date is considered here, choose +1 from desired end date as time is always considered as 00:00 for the end date selected.', null=True, verbose_name='End Date')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('remote_addr', models.CharField(blank=True, default='', max_length=100)),
                ('created_by', models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='windows_schedule_created_by_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Schedule',
                'verbose_name_plural': 'Schedules',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='ScheduleChoices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(max_length=30, verbose_name='Schedule Choice')),
            ],
            options={
                'verbose_name': 'Schedule Choice',
                'verbose_name_plural': 'Schedules Choices',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ScheduleDays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=30, verbose_name='Schedule Days')),
            ],
            options={
                'verbose_name': 'Schedule Day',
                'verbose_name_plural': 'Schedules Days',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ScheduleMonths',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(max_length=30, verbose_name='Schedule Months')),
            ],
            options={
                'verbose_name': 'Schedule Month',
                'verbose_name_plural': 'Schedules Months',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ScheduleMonthsDays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(help_text='Days on which schedule should run', max_length=30, verbose_name='Day of Month')),
            ],
            options={
                'verbose_name': 'Schedule Months Day',
                'verbose_name_plural': 'Schedules Months Days',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ScheduleMonthsOn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('on', models.CharField(help_text='FIRST/SECOND..LAST etc', max_length=30, verbose_name='Select On')),
            ],
            options={
                'verbose_name': 'Schedule Months On',
                'verbose_name_plural': 'Schedules Months On',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ScheduleMonthsOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(help_text='Days/On one of them is compulsary', max_length=30, verbose_name='Months Option')),
            ],
            options={
                'verbose_name': 'Schedule Months Option',
                'verbose_name_plural': 'Schedules Months Options',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='schedule',
            name='schedule_choice',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='windows_scheduler.ScheduleChoices', verbose_name='Schedule'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='schedule_option_month',
            field=models.ManyToManyField(blank=True, help_text='Month, if not specified all months will be considered', to='windows_scheduler.ScheduleMonths', verbose_name='Select Month'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='schedule_option_month_day',
            field=models.ForeignKey(default=1, help_text='Days, All Days By Default', on_delete=django.db.models.deletion.CASCADE, related_name='month_day_option', to='windows_scheduler.ScheduleMonthsDays', verbose_name='Select Days'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='schedule_option_month_on',
            field=models.ForeignKey(default=1, help_text='FIRST/SECOND..LAST etc', on_delete=django.db.models.deletion.CASCADE, related_name='month_on_option', to='windows_scheduler.ScheduleMonthsOn', verbose_name='Select On'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='schedule_option_month_on_day',
            field=models.ForeignKey(default=1, help_text='Sunday/Monday etc:', on_delete=django.db.models.deletion.CASCADE, related_name='month_on_day_option', to='windows_scheduler.ScheduleDays', verbose_name='Select On Day'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='schedule_option_month_option',
            field=models.ForeignKey(default=1, help_text='Days/On one of them is compulsary', on_delete=django.db.models.deletion.CASCADE, related_name='month_option', to='windows_scheduler.ScheduleMonthsOption', verbose_name='Months Option'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='schedule_option_week',
            field=models.ManyToManyField(blank=True, help_text='Day, if not selected all days will be considered', to='windows_scheduler.ScheduleDays', verbose_name='Weekly Option'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='updated_by',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='windows_updated_by_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
