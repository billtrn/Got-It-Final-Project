from marshmallow import fields
from marshmallow.validate import Length

from main.app import ma


class ItemSchema(ma.SQLAlchemySchema):
    id = fields.Int()
    name = fields.Str(validate=Length(max=45))
    description = fields.Str()

    class Meta:
        fields = ('id', 'name', 'description')