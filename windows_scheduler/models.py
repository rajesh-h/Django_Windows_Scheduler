from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
# Create your models here.

class ScheduleChoices(models.Model):
    choice = models.CharField(max_length=30,verbose_name='Schedule Choice')

    class Meta:
            ordering = ['id']
            verbose_name = "Schedule Choice"
            verbose_name_plural = "Schedules Choices"

    def __str__(self):              # __unicode__ on Python 2
        return self.choice

class ScheduleDays(models.Model):
    day = models.CharField(max_length=30,verbose_name='Schedule Days')

    class Meta:
            ordering = ['id']
            verbose_name = "Schedule Day"
            verbose_name_plural = "Schedules Days"

    def __str__(self):              # __unicode__ on Python 2
        return self.day

class ScheduleMonths(models.Model):
    month = models.CharField(max_length=30,verbose_name='Schedule Months')

    class Meta:
            ordering = ['id']
            verbose_name = "Schedule Month"
            verbose_name_plural = "Schedules Months"

    def __str__(self):              # __unicode__ on Python 2
        return self.month

class ScheduleMonthsOption(models.Model):
    option = models.CharField(max_length=30,verbose_name='Months Option',help_text="Days/On one of them is compulsary")

    class Meta:
            ordering = ['id']
            verbose_name = "Schedule Months Option"
            verbose_name_plural = "Schedules Months Options"

    def __str__(self):              # __unicode__ on Python 2
        return self.option

class ScheduleMonthsDays(models.Model):
    day = models.CharField(max_length=30,verbose_name='Day of Month',help_text="Days on which schedule should run")

    class Meta:
            ordering = ['id']
            verbose_name = "Schedule Months Day"
            verbose_name_plural = "Schedules Months Days"

    def __str__(self):              # __unicode__ on Python 2
        return self.day

class ScheduleMonthsOn(models.Model):
    on = models.CharField(max_length=30,verbose_name='Select On',help_text="FIRST/SECOND..LAST etc")

    class Meta:
            ordering = ['id']
            verbose_name = "Schedule Months On"
            verbose_name_plural = "Schedules Months On"

    def __str__(self):              # __unicode__ on Python 2
        return self.on


# Create your models here.
class Schedule(models.Model):
    schedule_name = models.CharField(max_length=100,unique=True,help_text="Unique Name For Schedule" )
    schedule_command = models.CharField( max_length=251, verbose_name='Schedule Command',help_text="Provide Your command to be run, it can be a full path to bat file")
    schedule_choice = models.ForeignKey('ScheduleChoices', verbose_name='Schedule',default=1)
    schedule_start = models.DateTimeField(default=datetime.now()+timedelta(minutes=30),blank=True,verbose_name='Start Time',help_text="Time 24 hours Format")
    schedule_option_repeat = models.BooleanField(default=False,verbose_name='Repeat Task',help_text="Do you want to Repeat Task on Some Interval?")
    schedule_option_task_interval = models.IntegerField(blank=True, null=True,verbose_name='Repeat Task Every',help_text="Task Interval if Applicable in Minutes (1 - 599940)")
    schedule_option_duration = models.CharField(max_length=10,blank=True, null=True,verbose_name='For a Duration Of',default="NA",help_text="Task Duraton to be run in HH:MM format, you can mention 120:00 as well for 5 days, indefinite Option Not provided for security purpose")
    schedule_option_recur = models.IntegerField(blank=True, null=True,verbose_name='Recur Every',help_text="Specify Recurrence", default=1)
    schedule_option_week = models.ManyToManyField('ScheduleDays',blank=True, verbose_name='Weekly Option',help_text="Day, if not selected all days will be considered")
    schedule_option_month = models.ManyToManyField('ScheduleMonths',blank=True, verbose_name='Select Month',help_text="Month, if not specified all months will be considered")
    schedule_option_month_option = models.ForeignKey('ScheduleMonthsOption', related_name='month_option',verbose_name='Months Option',help_text="Days/On one of them is compulsary",default=1)
    schedule_option_month_day   = models.ForeignKey('ScheduleMonthsDays',related_name='month_day_option', default=1, verbose_name='Select Days',help_text="Days, All Days By Default")
    schedule_option_month_on    = models.ForeignKey('ScheduleMonthsOn', related_name='month_on_option', default=1, verbose_name='Select On',help_text="FIRST/SECOND..LAST etc")
    schedule_option_month_on_day    = models.ForeignKey('ScheduleDays',default=1, related_name='month_on_day_option',verbose_name='Select On Day',help_text="Sunday/Monday etc:")
    schedule_end = models.DateTimeField(verbose_name='End Date',blank=True, null=True,help_text="Only date is considered here, choose +1 from desired end date as time is always considered as 00:00 for the end date selected.")
    created_by  = models.ForeignKey(User, related_name='windows_schedule_created_by_user',blank=True, null=True, default=None, editable=False)
    updated_by  = models.ForeignKey(User, related_name='windows_updated_by_user', blank=True, null=True, default=None, editable=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    remote_addr = models.CharField(blank=True, default='',max_length=100)

    class Meta:
            ordering = ["-updated_at"]
            verbose_name = "Schedule"
            verbose_name_plural = "Schedules"

    def __str__(self):              # __unicode__ on Python 2
        return self.schedule_name
