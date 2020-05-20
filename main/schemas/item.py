from marshmallow import fields
from marshmallow.validate import Length

from main.app import ma


class ItemSchema(ma.SQLAlchemySchema):
    id = fields.Int()
    name = fields.Str(required=True, validate=Length(max=45, error='Name must have under 45 characters.'))
    description = fields.Str()

    class Meta:
        fields = ('id', 'name', 'description')