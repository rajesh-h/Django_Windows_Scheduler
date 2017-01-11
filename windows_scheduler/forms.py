from django import forms
from django.utils import timezone
import datetime as dt
import subprocess
from django.core.exceptions import ValidationError
from .models import Schedule


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['schedule_name','schedule_command','schedule_start','schedule_choice',
                    'schedule_option_recur',
                    'schedule_option_week','schedule_option_month','schedule_option_month_option',
                    'schedule_option_month_day','schedule_option_month_on','schedule_option_month_on_day',
                    'schedule_option_repeat','schedule_option_task_interval','schedule_option_duration',
                    'schedule_end']


    def clean(self):
        cleaned_data = super(ScheduleForm, self).clean()
        #This is to check whether we have all the fields valid at first place, for eg time cannot be greater than 25 hours
        if not self.is_valid():
            return self.cleaned_data

        #get all form data entries
        #For new entry take from form, for existing entry take from model itself
        if not self.instance.pk:
            this_schedule_name           = cleaned_data.get('schedule_name')
        else:
            schedule                     = Schedule.objects.get(pk=self.instance.pk)
            this_schedule_name           = schedule.schedule_name
        this_schedule_command            = cleaned_data.get('schedule_command')
        this_schedule_start              = cleaned_data.get('schedule_start')
        this_schedule_choice             = cleaned_data.get('schedule_choice')
        this_schedule_option_recur       = cleaned_data.get('schedule_option_recur')
        this_schedule_option_week        = cleaned_data.get('schedule_option_week')
        this_schedule_option_month       = cleaned_data.get('schedule_option_month')
        this_schedule_option_month_option= cleaned_data.get('schedule_option_month_option')
        this_schedule_option_month_day   = cleaned_data.get('schedule_option_month_day')
        this_schedule_option_month_on    = cleaned_data.get('schedule_option_month_on')
        this_schedule_option_month_on_day= cleaned_data.get('schedule_option_month_on_day')
        this_schedule_option_repeat      = cleaned_data.get('schedule_option_repeat')
        this_schedule_option_task_interval = cleaned_data.get('schedule_option_task_interval')
        this_schedule_option_duration    = cleaned_data.get('schedule_option_duration')
        this_schedule_end                = cleaned_data.get('schedule_end')

        self.ScheduleTask(this_schedule_name,this_schedule_command,this_schedule_start,this_schedule_choice,this_schedule_option_recur,this_schedule_option_week,
                        this_schedule_option_month,this_schedule_option_month_option,this_schedule_option_month_day,this_schedule_option_month_on,this_schedule_option_month_on_day,
                        this_schedule_option_repeat,this_schedule_option_task_interval,this_schedule_option_duration,this_schedule_end)

    def ScheduleTask(self,this_schedule_name,this_schedule_command,this_schedule_start,this_schedule_choice,this_schedule_option_recur,this_schedule_option_week,
                    this_schedule_option_month,this_schedule_option_month_option,this_schedule_option_month_day,this_schedule_option_month_on,this_schedule_option_month_on_day,
                    this_schedule_option_repeat,this_schedule_option_task_interval,this_schedule_option_duration,this_schedule_end):
        if this_schedule_option_repeat:
            #check for various validations for this_schedule_option_task_interval and this_schedule_option_duration
            if this_schedule_option_task_interval in [None,""] or 0 >= this_schedule_option_task_interval or this_schedule_option_task_interval > 599940:
                self.RaiseValidationError('Error with Task Interval Value it should be between 1-599940')
            if this_schedule_option_duration in [None,"",'NA','na','Na']:
                self.RaiseValidationError('Task Duration Cannot be null/blank/NA if you have selected Task Repeat option')
            try:
                if this_schedule_option_duration[-3] != ':':
                    self.RaiseValidationError('Task Duration should be in HH:MM format')
            except Exception as e:
                self.RaiseValidationError('Invalid Data provided for Task Duration')
            if not this_schedule_option_duration.replace(':','').isdigit():
                self.RaiseValidationError('Task Duration should be in HH:MM format')
            if int(this_schedule_option_duration.replace(':','')) <= 0:
                self.RaiseValidationError('Task Duration should be greater than 00:00')

        if this_schedule_start <= timezone.make_aware(dt.datetime.now(), timezone.get_default_timezone()):
            self.RaiseValidationError('Please select Start date/Time greater than curremt time')

        #get the start date
        start_date = this_schedule_start.strftime('%Y-%m-%d')
        #get start time
        start_time = this_schedule_start.strftime('%H:%M')


        if this_schedule_choice.choice == 'One Time':
            print ('Scheduling One Time Event')

            if not this_schedule_option_repeat:
                command = ['Schtasks.exe', '/Create', '/SC', 'ONCE','/SD', start_date,  '/ST', start_time, '/TN', this_schedule_name, '/F', '/TR',this_schedule_command ]
                self.TaskSetup(command)
            else:
                command = ['Schtasks.exe', '/Create', '/SC', 'ONCE','/SD', start_date,  '/ST', start_time, '/RI',str(this_schedule_option_task_interval), '/DU', this_schedule_option_duration,  '/TN', this_schedule_name, '/F', '/TR',this_schedule_command ]
                self.TaskSetup(command)

        elif this_schedule_choice.choice == 'Daily':
            print ('Scheduling Daily Event')
            if not this_schedule_end:
                self.RaiseValidationError('End Date/Time Mnadatory for this option')
            if this_schedule_end <= this_schedule_start:
                self.RaiseValidationError('Scheule End Date/Time should be greater than Start date/Time')
            #get the End date
            end_date = this_schedule_end.strftime('%Y-%m-%d')

            if not this_schedule_option_repeat:
                command = ['Schtasks.exe', '/Create', '/SC', 'DAILY','/SD', start_date,  '/ST', start_time, '/ED', end_date,
                '/MO', str(this_schedule_option_recur),  '/TN', this_schedule_name, '/F', '/TR',this_schedule_command ]
                self.TaskSetup(command)
            else:
                command =  ['Schtasks.exe', '/Create', '/SC', 'DAILY','/SD', start_date,  '/ST', start_time, '/ED', end_date, '/RI',str(this_schedule_option_task_interval),
                '/DU', this_schedule_option_duration, '/MO', str(this_schedule_option_recur),  '/TN', this_schedule_name, '/F', '/TR',this_schedule_command ]
                self.TaskSetup(command)

        elif this_schedule_choice.choice == 'Weekly':
            print ('Scheduling Weekly Event')
            if not this_schedule_end:
                self.RaiseValidationError('End Date/Time Mnadatory for this option')
            if this_schedule_end <= this_schedule_start:
                self.RaiseValidationError('Scheule End Date/Time should be greater than Start date/Time')
            #get the End date
            end_date = this_schedule_end.strftime('%Y-%m-%d')

            #Get days of the weeks if provided else use all 7 days
            days_scheduled = this_schedule_option_week.all()
            days_list = []
            for day in days_scheduled:
                days_list.append(str(day))
            if len(days_list) > 0:
                req_days = ",".join(days_list)
            else:
                req_days = "*"
            print (req_days)

            if not this_schedule_option_repeat:
                command = ['Schtasks.exe', '/Create', '/SC', 'WEEKLY','/SD', start_date,  '/ST', start_time, '/ED', end_date,  '/D', req_days,
                '/MO', str(this_schedule_option_recur),  '/TN', this_schedule_name, '/F', '/TR',this_schedule_command ]
                self.TaskSetup(command)
            else:
                command =  ['Schtasks.exe', '/Create', '/SC', 'WEEKLY','/SD', start_date,  '/ST', start_time, '/ED', end_date, '/RI',str(this_schedule_option_task_interval),
                '/DU', this_schedule_option_duration, '/D', req_days, '/MO', str(this_schedule_option_recur),  '/TN', this_schedule_name, '/F', '/TR',this_schedule_command ]
                self.TaskSetup(command)

        elif this_schedule_choice.choice == 'Monthly':
            print ('Scheduling Monthly Event')
            if not this_schedule_end:
                self.RaiseValidationError('End Date/Time Mnadatory for this option')
            if this_schedule_end <= this_schedule_start:
                self.RaiseValidationError('Scheule End Date/Time should be greater than Start date/Time')
            #get the End date
            end_date = this_schedule_end.strftime('%Y-%m-%d')

            #Get Months  if provided else use all 12 months using *
            months_scheduled = this_schedule_option_month.all()
            months_list = []
            for month in months_scheduled:
                months_list.append(str(month))
            if len(months_list) > 0:
                req_months = ",".join(months_list)
            else:
                req_months = "*"
            print (req_months)


            #This is where it is pending now
            if not this_schedule_option_repeat:
                if str(this_schedule_option_month_option) == 'Days':
                    if this_schedule_option_month_day.day != 'LastDay':
                        command = ['Schtasks.exe', '/Create', '/SC', 'MONTHLY','/SD', start_date,  '/ST', start_time, '/ED', end_date, '/M', req_months, '/D', this_schedule_option_month_day.day,
                            '/TN', this_schedule_name, '/F', '/TR',this_schedule_command ]
                    else:
                        command = ['Schtasks.exe', '/Create', '/SC', 'MONTHLY','/SD', start_date,  '/ST', start_time, '/ED', end_date, '/M', req_months, '/MO', this_schedule_option_month_day.day,
                            '/TN', this_schedule_name, '/F', '/TR',this_schedule_command ]
                else:
                    command = ['Schtasks.exe', '/Create', '/SC', 'MONTHLY','/SD', start_date,  '/ST', start_time, '/ED', end_date, '/M', req_months, '/D', this_schedule_option_month_on_day.day,
                            '/MO', this_schedule_option_month_on.on, '/TN', this_schedule_name, '/F', '/TR',this_schedule_command ]

                self.TaskSetup(command)
            else:
                if str(this_schedule_option_month_option) == 'Days':
                    if this_schedule_option_month_day.day != 'LastDay':
                        command = ['Schtasks.exe', '/Create', '/SC', 'MONTHLY','/SD', start_date,  '/ST', start_time, '/ED', end_date, '/M', req_months, '/D', this_schedule_option_month_day.day,
                        '/RI',str(this_schedule_option_task_interval),'/DU', this_schedule_option_duration, '/TN', this_schedule_name, '/F', '/TR',this_schedule_command ]
                    else:
                        command = ['Schtasks.exe', '/Create', '/SC', 'MONTHLY','/SD', start_date,  '/ST', start_time, '/ED', end_date, '/M', req_months, '/MO', this_schedule_option_month_day.day,
                            '/RI',str(this_schedule_option_task_interval),'/DU', this_schedule_option_duration, '/TN', this_schedule_name, '/F', '/TR',this_schedule_command ]

                else:
                    command = ['Schtasks.exe', '/Create', '/SC', 'MONTHLY','/SD', start_date,  '/ST', start_time, '/ED', end_date, '/M', req_months, '/D', this_schedule_option_month_on_day.day,
                            '/RI',str(this_schedule_option_task_interval),'/DU', this_schedule_option_duration, '/MO', this_schedule_option_month_on.on, '/TN', this_schedule_name, '/F', '/TR',this_schedule_command ]

                self.TaskSetup(command)



        else:
            ErrorMessage = 'Please note: Choice "' + this_schedule_choice.choice + '" is not catered for yet'
            print (ErrorMessage)
            raise ValidationError(ErrorMessage)

    def TaskSetup(self,command):
        #This is to avoid repeating this again and again at each level
        try:
            #Schedule the task
            command_output = subprocess.check_output(command)
            return self.cleaned_data
        except Exception as e:
            ErrorMessage = 'Could not schedule this task Please Contact Admin'
            print (ErrorMessage)
            print (str(e))
            raise ValidationError(ErrorMessage)

    def RaiseValidationError(self,Message):
        ErrorMessage = Message
        print (ErrorMessage)
        raise ValidationError(ErrorMessage)
