from django.http.response import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .models import Attendances
from django.db.models import Sum
from datetime import date, datetime, timedelta


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    login_url = '/accounts/login/'


class PushTimecard(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'

    def post(self, request, *args, **kwargs):
        push_type = request.POST.get('push_type')

        is_attendanced = Attendances.objects.filter(
            user=request.user,
            attendance_time__date=date.today()
        ).exists()
        is_left = Attendances.objects.filter(
            user=request.user,
            leave_time__date=date.today()
        ).exists()

        response_body = {}
        if push_type == 'attendance' and not is_attendanced:
            attendance = Attendances(user=request.user)
            attendance.save()
            response_time = attendance.attendance_time
            response_body = {
                'result': 'success',
                'attendance_time': response_time.strftime('%Y-%m-%d %H:%M')
            }
        elif push_type == 'leave' and not is_left:
            if is_attendanced:
                attendance = Attendances.objects.filter(
                    user=request.user,
                    attendance_time__date=date.today()
                ).first()  # 最初のレコードを取得するには `.first()` を使用します
                attendance.leave_time = datetime.now()
                attendance.save()
                response_time = attendance.leave_time
                response_body = {
                    'result': 'success',
                    'leave_time': response_time.strftime('%Y-%m-%d %H:%M')
                }
            else:
                response_body = {
                    'result': 'not_attended',
                }
        if not response_body:
            response_body = {
                'result': 'already_exists'
            }
        return JsonResponse(response_body)


class AttendanceRecords(LoginRequiredMixin, TemplateView):
    template_name = 'attend_records.html'
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        today = datetime.today()
        search_param = request.GET.get('year_month')
        if search_param:
            search_param = list(map(int, search_param.split('-')))
            search_year = search_param[0]
            search_month = search_param[1]
        else:
            search_year = today.year
            search_month = today.month

        month_attendances = Attendances.objects.filter(
            user=request.user,
            attendance_time__year=search_year,
            attendance_time__month=search_month
        ).order_by('attendance_time')

        attendances_context = []
        total_work_duration = timedelta()

        for attendance in month_attendances:
            attendance_time = attendance.attendance_time
            leave_time = attendance.leave_time
            if leave_time:
                leave_time_str = leave_time.strftime('%H:%M')
            else:
                if attendance_time.date() == today.date():
                    leave_time_str = None
                else:
                    leave_time_str = 'not_pushed'

            work_duration = attendance.work_duration
            if work_duration:
                total_work_duration += work_duration

            day_attendance = {
                'date': attendance_time.strftime('%Y-%m-%d'),
                'attendance_at': attendance_time.strftime('%H:%M'),
                'leave_at': leave_time_str,
                'work_duration': attendance.formatted_work_duration(),
                'total_work_seconds': int(work_duration.total_seconds()) if work_duration else 0
            }
            attendances_context.append(day_attendance)

        # 月間の合計労働時間の計算（「時:分」形式）
        total_seconds = int(total_work_duration.total_seconds())
        total_hours = total_seconds // 3600
        total_minutes = (total_seconds % 3600) // 60
        total_work_duration_str = f"{total_hours:02}:{total_minutes:02}"

        context = {
            'attendances': attendances_context,
            'total_work_duration': total_work_duration_str
        }
        return self.render_to_response(context)
