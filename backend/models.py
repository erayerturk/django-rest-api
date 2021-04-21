from enum import Enum

from django.db import models

# Create your models here.
from tayf_auth.models import CustomUser


class NoteStatus(Enum):
    ACTIVE = 0
    DELETED = 1


class Notes(models.Model):
    subject = models.CharField(max_length=50)
    note = models.CharField(max_length=255)
    alarm_at = models.DateTimeField(default=None, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=NoteStatus.ACTIVE.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.subject

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'


class Files(models.Model):
    notes = models.ForeignKey(Notes, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to="files/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
