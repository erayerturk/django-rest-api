import datetime
from typing import List

import pytz as pytz
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.files import UploadedFile
from ninja import File
from django.core.paginator import Paginator

from backend.models import Notes, NoteStatus, Files
from backend.schemas import NoteSchema, ErrorMessage, NoteCreateSchema, NoteListSchema, UserListSchema, \
    UserSchema, UserUpdateSchema, ResultSchema, FileSchema
from tayf_auth.api import TokenAuth
from tayf_auth.models import CustomUser

router = Router()


@router.post('/add-note', response={201: NoteSchema, 401: ErrorMessage}, auth=TokenAuth())
def add_note(request, payload: NoteCreateSchema):
    user: CustomUser = get_object_or_404(CustomUser, pk=request.user_id)
    if user:
        data = payload.dict()
        if 'user_id' in data.keys() and user.is_staff:
            data['user'] = get_object_or_404(CustomUser, pk=payload.user_id)
        else:
            data['user'] = get_object_or_404(CustomUser, pk=request.user_id)

        note = Notes.objects.create(**data)

        return 201, note

    return 401, {"errors": {'error': 'Can not create'}}


@router.post("/upload", response={200: ResultSchema, 401: ErrorMessage}, auth=TokenAuth())
def upload(request, note_id: int, name: str, file: UploadedFile = File(...)):
    user: CustomUser = get_object_or_404(CustomUser, pk=request.user_id)
    if user or user.is_staff:
        note = get_object_or_404(Notes, pk=note_id)
        file = Files.objects.create(notes=note, name=name, file=file)
        return 200, {'result': f"{file.name} uploaded"}
    return 401, {"errors": {'error': 'Can not create'}}


@router.delete('/delete-note/{note_id}', response={204: ResultSchema, 401: ErrorMessage}, auth=TokenAuth())
def delete_note(request, note_id: int):
    note = get_object_or_404(Notes, pk=note_id)
    user = get_object_or_404(CustomUser, pk=request.user_id)

    if user or user.is_staff:
        note.status = NoteStatus.DELETED.value
        note.save()
        return 204, {"result": "Deleted"}
    return 401, {"errors": {'error': 'Can not delete'}}


@router.put('/update-note/{note_id}', response={204: NoteSchema, 401: ErrorMessage}, auth=TokenAuth())
def update_note(request, note_id: int, payload: NoteSchema):
    note = get_object_or_404(Notes, pk=note_id)
    user = get_object_or_404(CustomUser, pk=request.user_id)

    if user or user.is_staff:
        note.subject = payload.subject
        note.note = payload.note
        note.alarm_at = payload.alarm_at
        note.save()
        return 204, note
    return 401, {"errors": {'error': 'Can not update'}}


@router.get('/list-note/{user_id}', response={200: NoteListSchema, 401: ErrorMessage}, auth=TokenAuth())
def list_notes(request, user_id: int, per_page: int, page: int):
    user = get_object_or_404(CustomUser, pk=request.user_id)

    if user or user.is_staff:
        paginator = Paginator(Notes.objects.filter(user=user_id, status=NoteStatus.ACTIVE.value), per_page)
        notes: List[Notes] = list(paginator.get_page(page).object_list)
        return 200, {"per_page": per_page, "page": page, "notes": notes}
    return 401, {"errors": {'error': 'Can not list'}}


# Admin

@router.get('/list-users/', response={200: UserListSchema, 401: ErrorMessage}, auth=TokenAuth())
def list_users(request, per_page: int, page: int):
    user = get_object_or_404(CustomUser, pk=request.user_id)

    if user.is_staff:
        paginator = Paginator(CustomUser.objects.all(), per_page)
        users: List[CustomUser] = list(paginator.get_page(page).object_list)
        return 200, {"per_page": per_page, "page": page, "users": users}
    return 401, {'errors': {'auth': 'Unauthorized'}}


@router.post('/add-user/', response={201: UserSchema, 401: ErrorMessage}, auth=TokenAuth())
def add_user(request, payload: UserSchema):
    user = get_object_or_404(CustomUser, pk=request.user_id)
    if user.is_staff:
        data = payload.dict()
        user = CustomUser.objects.create(**data)
        return 201, user
    return 401, {'errors': {'auth': 'Unauthorized'}}


@router.delete('/delete-user/{user_id}', response={204: ResultSchema, 401: ErrorMessage}, auth=TokenAuth())
def delete_user(request, user_id: int):
    user = get_object_or_404(CustomUser, pk=request.user_id)
    if user.is_staff:
        del_user = get_object_or_404(CustomUser, pk=user_id)
        del_user.is_deleted = True
        del_user.save()
        return 204, {"result": "Deleted"}
    return 401, {'errors': {'auth': 'Unauthorized'}}


@router.put('/update-user/{user_id}', response={204: UserSchema, 401: ErrorMessage}, auth=TokenAuth())
def update_user(request, user_id: int, payload: UserUpdateSchema):
    user = get_object_or_404(CustomUser, pk=request.user_id)
    if user.is_staff:
        update_user = get_object_or_404(CustomUser, pk=user_id)
        update_user.email = payload.email
        update_user.set_password(payload.password)
        update_user.first_name = payload.first_name
        update_user.last_name = payload.last_name
        update_user.is_active = payload.is_active
        update_user.is_deleted = payload.is_deleted
        update_user.is_staff = payload.is_staff
        update_user.is_superuser = payload.is_superuser
        update_user.save()
        return 204, update_user
    return 401, {'errors': {'auth': 'Unauthorized'}}


@router.get('/get-online-count/', response={200: ResultSchema, 401: ErrorMessage}, auth=TokenAuth())
def get_online_count(request):
    _user = get_object_or_404(CustomUser, pk=request.user_id)
    if _user.is_staff:
        users: List[CustomUser] = list(CustomUser.objects.all())
        now = datetime.datetime.now(tz=pytz.utc)
        ten_minutes_before = now - datetime.timedelta(minutes=10)
        online_count = 0
        for user in users:
            if user.last_logged_in.timestamp() >= ten_minutes_before.timestamp():
                online_count += 1

        return 200, {"result": online_count}
    return 401, {'errors': {'auth': 'Unauthorized'}}
