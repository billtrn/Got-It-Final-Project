from marshmallow import fields
from marshmallow.validate import Length

from main.schemas.base import BaseSchema


class ItemSchema(BaseSchema):
    id = fields.Int()
    name = fields.Str(required=True, validate=Length(min=1, max=45, error='Name must have between 1-45 characters.'))
    description = fields.Str()
    created_on = fields.DateTime(dump_only=True)
    updated_on = fields.DateTime(dump_only=True)

    class Meta:
        fields = ('id', 'name', 'description', 'created_on', 'updated_on')
