from marshmallow import fields
from marshmallow.validate import Length

from main.app import ma


class ItemSchema(ma.SQLAlchemySchema):
    id = fields.Int()
    name = fields.Str(required=True, validate=Length(min=1, max=45, error='Name must have between 1-45 characters.'))
    description = fields.Str()

    class Meta:
        fields = ('id', 'name', 'description')
