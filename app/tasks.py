from huey import crontab
from huey.contrib.djhuey import db_periodic_task
from .models import Photo, UserTopNotifyMessage
from django.core.mail import send_mass_mail
from django.conf import settings


def collect_top_users_emails(top_viewed) -> set:
    user_emails = set()

    def add_users_email_to_top(top, max_views=0):
        """Добавление имейла юзера в множество если его фото в топе просмотренных"""
        if not top:
            return

        if not max_views:
            max_views = Photo.objects.all().order_by('viewed').last().viewed
        else:
            max_views = Photo.objects.filter(viewed__lt=max_views).order_by('viewed').last().viewed
        if not max_views:
            return

        for p in Photo.objects.filter(viewed=max_views):
            user_emails.add(p.owner.email)

        top -= 1
        add_users_email_to_top(top, max_views)

    add_users_email_to_top(top_viewed)
    return user_emails


@db_periodic_task(crontab(minute='0', hour='9', day='*/1'))
def send_emails_top_site_photos():
    """Отправка письма юзеру каждый день в 9 утра о том что его фото в топ 3 сайта"""
    message = UserTopNotifyMessage.objects.all()[0]
    message_list = []
    user_emails = collect_top_users_emails(settings.TOP_VIEWED_PHOTOS)
    for email in user_emails:
        message_list.append((message.subject, message.message, message.from_email, [email]))
    if message_list:
        send_mass_mail(message_list, fail_silently=False)
    return 0
