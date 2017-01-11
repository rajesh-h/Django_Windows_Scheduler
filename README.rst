=====
Windows_Scheduler
=====

Windows_Scheduler is a simple Django app to schedule tasks on a windows machine using the built in Windows Task Scheduler

This will provide an interface for the users of your application to setup the tasks without logging into your server and accessing TaskScheduler
Task which needs to be setup(Eg: Send_Disk_usage_report.bat) should be setup in the server by admin or the user who has access to the server.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "windows_scheduler" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'windows_scheduler',
    ]

2. Run `python manage.py migrate` to create the windows_scheduler models.

3. Run `python manage.py loaddata windows_scheduler_fixture.json` to load some initial data for the windows_scheduler models.

4. Run `python manage.py collectstatic` to load static files related to windows_scheduler app.

5. Start the development server and visit http://127.0.0.1:8000/admin/windows_scheduler/
   to create a schedules (you'll need the Admin app enabled).

6. Visit http://127.0.0.1:8000/admin/windows_scheduler/schedules to create the schedule.
