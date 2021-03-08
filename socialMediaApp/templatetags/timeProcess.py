from django import template
import datetime
import pytz

register = template.Library()


@register.simple_tag
def timeProcess(post_time):
    now = datetime.datetime.now(pytz.UTC)

    if (now.year == post_time.year and
            now.month == post_time.month and
            now.day == post_time.day and
            now.hour == post_time.hour and
            now.minute == post_time.minute and
            now.second == post_time.second and
            now.microsecond != post_time.microsecond):
        return "کمی پیش"
    elif (now.year == post_time.year and
            now.month == post_time.month and
            now.day == post_time.day and
            now.hour == post_time.hour and
            now.minute == post_time.minute and
            now.second != post_time.second):
        return "کمی پیش"
    elif (now.year == post_time.year and
            now.month == post_time.month and
            now.day == post_time.day and
            now.hour == post_time.hour and
            now.minute != post_time.minute):
        return "کمی پیش"
    elif(now.year == post_time.year and
            now.month == post_time.month and
            now.day == post_time.day and
            now.hour != post_time.hour):
        ans = "ساعت پیش {}".format(now.hour - post_time.hour)
        return ans
    elif(now.year == post_time.year and
            now.month == post_time.month and
            now.day != post_time.day):
        ans = "روز پیش {}".format(now.day - post_time.day)
        return ans
    elif(now.year == post_time.year and
            now.month != post_time.month):
        ans = "ماه پیش {}".format(now.month - post_time.month)
        return ans
    else:
        return "خیلی وقت پیش"




