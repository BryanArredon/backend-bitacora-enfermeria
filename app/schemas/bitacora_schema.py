from marshmallow import Schema, fields, validate, ValidationError, validates_schema
from datetime import datetime


def validate_iso_datetime(value):
    try:
        datetime.fromisoformat(value)
    except ValueError:
        raise ValidationError("Formato de fecha inválido. Usa ISO 8601.")


class BitacoraSchema(Schema):
    paciente_id = fields.UUID(
        required=True,
        error_messages={"required": "El paciente_id es obligatorio"}
    )

    enfermero_id = fields.UUID(
        required=True,
        error_messages={"required": "El enfermero_id es obligatorio"}
    )

    turno = fields.Str(
        required=True,
        validate=validate.OneOf(["matutino", "vespertino", "nocturno"]),
        error_messages={"required": "El turno es obligatorio"}
    )

    signos_vitales = fields.Dict(
        required=False,
        load_default={}
    )

    observaciones = fields.Str(
        required=True,
        validate=validate.Length(min=5),
        error_messages={"required": "Las observaciones son obligatorias"}
    )

    medicamentos_administrados = fields.List(
        fields.Str(),
        required=False,
        load_default=[]
    )

    cliente_timestamp = fields.Str(
        required=True,
        validate=validate_iso_datetime,
        error_messages={"required": "El timestamp es obligatorio"}
    )

    # Seguridad: bloquear campos extra
    class Meta:
        unknown = "RAISE"

    # Validaciones avanzadas
    @validates_schema
    def validate_logica_negocio(self, data, **kwargs):

        signos = data.get("signos_vitales", {})
        if signos and not isinstance(signos, dict):
            raise ValidationError("signos_vitales debe ser un objeto JSON válido")

        meds = data.get("medicamentos_administrados", [])
        if meds and not isinstance(meds, list):
            raise ValidationError("medicamentos_administrados debe ser una lista")

        for m in meds:
            if not m or not isinstance(m, str):
                raise ValidationError("Los medicamentos deben ser strings válidos")