from marshmallow import Schema, pre_load


class BaseSchema(Schema):
    @pre_load
    def strip_input(self, data, **_):
        for key, value in data.items():
            if type(value) is str:
                data[key] = data[key].strip()
        return data
