from flask_marshmallow import Marshmallow
from marshmallow import fields, validate

ma = Marshmallow()

class AulaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Aula
        load_instance = True

    titulo = fields.String(required=True, validate=validate.Length(min=3))
    disciplina = fields.String(required=True)
    data_prevista = fields.Date(required=True)