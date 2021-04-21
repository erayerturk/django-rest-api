import datetime
from typing import Dict, Any, List

import pytz
from ninja import Schema
from ninja.orm import create_schema

from backend.models import Notes, Files
from tayf_auth.models import CustomUser

UserSchema = create_schema(CustomUser)
NoteSchema = create_schema(Notes)

UserUpdateSchema = create_schema(CustomUser, exclude=['id', 'last_login', 'last_logged_in', 'date_joined', 'groups',
                                                      'user_permissions'])


class NoteCreateSchema(Schema):
    subject: str
    note: str
    user_id: int
    alarm_at: str = str(datetime.datetime.now(tz=pytz.UTC).isoformat())
    status: int


class FileSchema(Schema):
    file: str
    name: str


class ErrorMessage(Schema):
    errors: Dict[str, Any]


class ResultSchema(Schema):
    result: str


class NoteListSchema(Schema):
    per_page: int
    page: int
    notes: List[NoteSchema] = []


class UserListSchema(Schema):
    per_page: int
    page: int
    users: List[UserSchema] = []
