from marshmallow import fields
from marshmallow.validate import Length

from main.schemas.base import BaseSchema


class UserSchema(BaseSchema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=Length(min=1, max=45,
                                                         error='Username must have between 1-45 characters.'))
    password = fields.Str(required=True, validate=Length(min=1, max=45,
                                                         error='Password must have between 1-45 characters.'))

    class Meta:
        fields = ('id', 'username', 'password')


class UserAuthenticationSchema(BaseSchema):
    username = fields.Str(required=True, validate=Length(max=45))
    access_token = fields.Str(required=True, dump_only=True)
    id = fields.Int()

    class Meta:
        fields = ('username', 'access_token', 'id')
