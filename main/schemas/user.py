from marshmallow import fields
from marshmallow.validate import Length

from main.app import ma


class UserSchema(ma.SQLAlchemySchema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=Length(max=45, error='Username must have under 45 characters.'))
    password = fields.Str(required=True, validate=Length(max=45, error='Password must have under 45 characters.'))

    class Meta:
        fields = ('id', 'username', 'password')


class UserAuthenticationSchema(ma.SQLAlchemySchema):
    username = fields.Str(required=True, validate=Length(max=45))
    access_token = fields.Str(required=True, dump_only=True)
    id = fields.Int()

    class Meta:
        fields = ('username', 'access_token', 'id')
