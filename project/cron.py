from datetime import datetime, timedelta
from typing import List

import pytz as pytz
from django.core.mail import send_mail

from backend.models import Notes


def note_alarm():
    notes: List[Notes] = list(Notes.objects.all())
    for note in notes:
        now = datetime.now(tz=pytz.utc)
        before = now - timedelta(seconds=30)
        after = now + timedelta(seconds=30)
        if before <= note.alarm_at <= after:
            send_mail(f"Alarm! {note.subject}", note.note, 'no-reply@erayerturk.com', [note.user.email],
              fail_silently=False, )

# python manage.py crontab add
# python manage.py crontab show
# python manage.py crontab remove
