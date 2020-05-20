from marshmallow import fields
from marshmallow.validate import Length

from main.app import ma


class UserSchema(ma.SQLAlchemySchema):
    id = fields.Int(dump_only=True)
    username = fields.Str(validate=Length(max=45))
    password = fields.Str(validate=Length(max=45))

    class Meta:
        fields = ('id', 'username', 'password')


class UserAuthenticationSchema(ma.SQLAlchemySchema):
    username = fields.Str(validate=Length(max=45))
    access_token = fields.Str(required=True, dump_only=True)
    id = fields.Int()

    class Meta:
        fields = ('username', 'access_token', 'id')
