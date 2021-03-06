from marshmallow import fields
from marshmallow.validate import Length

from main.schemas.base import BaseSchema


class CategorySchema(BaseSchema):
    id = fields.Int()
    name = fields.Str(
        required=True,
        validate=Length(min=1, max=45, error='Name must have between 1-45 characters.')
    )
    description = fields.Str(missing='')
    created = fields.DateTime(dump_only=True)
