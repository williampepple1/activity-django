from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime

# Define the function
def get_default_end_date():
    return datetime.now().date() + timedelta(days=7)
def get_current_week_start():
    """Calculate the start date (Monday) of the current week."""
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    return start_of_week

def get_current_week_end():
    """Calculate the end date (Sunday) of the current week."""
    start_of_week = get_current_week_start()
    end_of_week = start_of_week + timedelta(days=6)  # Sunday
    return end_of_week

class Week(models.Model):
    start_date = models.DateField(default=get_current_week_start)
    end_date = models.DateField(default=get_current_week_end)

class Activity(models.Model):
    name = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    deadline = models.DateField(default=get_default_end_date)
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
