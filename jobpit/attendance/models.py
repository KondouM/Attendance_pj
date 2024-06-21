from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class Attendances(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attendance_time = models.DateTimeField(default=datetime.now)
    leave_time = models.DateTimeField(null=True)
    work_duration = models.DurationField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.leave_time:
            self.work_duration = self.leave_time - self.attendance_time
        else:
            self.work_duration = timedelta(0)
        super().save(*args, **kwargs)

    def formatted_work_duration(self):
        if self.work_duration:
            total_seconds = int(self.work_duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02}:{minutes:02}"
        return "00:00:00"

    def __str__(self):
        return f"{self.user.username} - {self.attendance_time}"
