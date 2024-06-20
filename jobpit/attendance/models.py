from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from datetime import timedelta

class Attendances(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attendance_time = models.DateTimeField(default=datetime.now)
    leave_time = models.DateTimeField(null=True)

    @property
    def work_duration(self):
        if self.leave_time:
            return self.leave_time - self.attendance_time
        return timedelta(0)

    def formatted_work_duration(self):
        work_duration = self.work_duration
        total_seconds = int(work_duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"