from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from datetime import datetime
# Register your models here.
from .forms import ScheduleForm
from .models import Schedule, ScheduleChoices, ScheduleDays, ScheduleMonths,ScheduleMonthsOption,ScheduleMonthsDays,ScheduleMonthsOn

#admin.site.register(ScheduleChoices)
#admin.site.register(ScheduleDays)
#admin.site.register(ScheduleMonths)
#admin.site.register(ScheduleMonthsOption)
#admin.site.register(ScheduleMonthsDays)
#admin.site.register(ScheduleMonthsOn)

class ScheduleAdmin(admin.ModelAdmin):
    model = Schedule
    #readonly_fields = ['schedule_name',]
    radio_fields = {"schedule_choice": admin.HORIZONTAL,'schedule_option_month_option':admin.HORIZONTAL ,'schedule_option_month_day':admin.HORIZONTAL
                        ,'schedule_option_month_on':admin.HORIZONTAL, 'schedule_option_month_on_day':admin.HORIZONTAL,}
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    #filter_horizontal = ['schedule_option_week',]
    #filter_vertical = ['schedule_option_week',]
    fields = [('schedule_name','schedule_command',),'schedule_start','schedule_choice',
                'schedule_option_recur',
                'schedule_option_week','schedule_option_month','schedule_option_month_option',
                'schedule_option_month_day','schedule_option_month_on','schedule_option_month_on_day',
                'schedule_option_repeat',('schedule_option_task_interval','schedule_option_duration',),
                'schedule_end']
    exclude = ('remote_addr',)
    list_display = ['schedule_name','schedule_command','schedule_choice','updated_by','updated_at',]
    save_as = True
    #using below form to make other necessary cecks before saving the model
    form = ScheduleForm

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
            obj.updated_at = datetime.now()
            obj.remote_addr = request.META['REMOTE_ADDR']
        else:
            obj.created_by = request.user
            obj.created_at = datetime.now()
            obj.updated_by = request.user
            obj.remote_addr = request.META['REMOTE_ADDR']
        obj.save()

    #Make a field readOnly for update view
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('schedule_name',)
        return self.readonly_fields


admin.site.register(Schedule,ScheduleAdmin)
