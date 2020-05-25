import re

from marshmallow import fields, ValidationError
from marshmallow.validate import Length

from main.schemas.base import BaseSchema


def _validate_username(string):
    regex = re.compile('^[A-Za-z0-9]+$')
    if not regex.match(string):
        raise ValidationError('Username must contain only letters and numbers.')


class UserSchema(BaseSchema):
    id = fields.Int(dump_only=True)
    username = fields.Str(
        required=True,
        validate=[_validate_username, Length(min=1, max=45, error='Username must have between 1-45 characters.')]
    )
    password = fields.Str(
        required=True,
        validate=Length(min=1, max=45, error='Password must have between 1-45 characters.')
    )
    created = fields.DateTime(dump_only=True)


class UserAuthenticationSchema(BaseSchema):
    id = fields.Int(dump_only=True)
    username = fields.Str(dump_only=True)
    access_token = fields.Str(dump_only=True)
