from typing import Any, Dict

from ninja import Schema
from ninja.orm import create_schema
from tayf_auth import models

UserAuthSchema = create_schema(models.CustomUser,
                               fields=['id', 'email', 'first_name', 'last_name', 'sex'])

UserProfileSchema = create_schema(models.CustomUser,
                                  fields=['email', 'first_name', 'sex', 'last_name'])

EditProfileResponseSchema = create_schema(models.CustomUser,
                                          fields=['email', 'first_name', 'last_name'])


class AccessTokenSchema(Schema):
    access_token: str


class ErrorMessage(Schema):
    errors: Dict[str, Any]


class MailConfirmedSchema(Schema):
    result: str


class LoginSchema(Schema):
    username: str
    password: str


class RegisterSchema(Schema):
    email: str
    first_name: str
    last_name: str
    sex: int
    password1: str
    password2: str


class PasswordSchema(Schema):
    result: Dict[str, Any]


class ResetPasswordSchema(Schema):
    email: str


class ResetPasswordResponseSchema(Schema):
    result: str
