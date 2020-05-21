from marshmallow import pre_load

from main.app import ma


class BaseSchema(ma.SQLAlchemySchema):
    @pre_load
    def strip_input(self, data, **kwargs):
        for key, value in data.items():
            if type(value) is str:
                data[key] = data[key].strip()
        return data
