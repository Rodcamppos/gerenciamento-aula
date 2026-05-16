from flask_marshmallow import Marshmallow
from marshmallow import fields, validate
from .models import Aula

ma = Marshmallow()

class AulaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Aula
        load_instance = True
        include_fk = True

    titulo = fields.String(required=True, validate=validate.Length(min=3))
    disciplina = fields.String(required=True)
    objetivo = fields.String(required=True, validate=validate.Length(min=10))
    ementa = fields.String(required=True, validate=validate.Length(min=10))
    data_prevista = fields.Date(required=True)
    tags = fields.String(allow_none=True)