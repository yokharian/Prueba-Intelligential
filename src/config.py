"""create in-memory database"""
from os import getenv

from sqlalchemy import (
    Table,
    Column,
    Integer,
    CheckConstraint,
    DateTime,
    Float,
    Boolean,
    create_engine,
    MetaData,
)

PRODUCTION = getenv("PRODUCTION", False)
IN_MEMORY_DATABASE = False if getenv("IN_MEMORY_DATABASE", False) == 'False' else True
DATE_FORMAT = "%d-%m-%Y"

DATABASE_PATH = '/storage.db' if IN_MEMORY_DATABASE is False else ''
engine = create_engine("sqlite://" + DATABASE_PATH, echo=False)

meta = MetaData()
pago = Table(
    "PAGO",
    meta,
    Column("id_pago", Integer, primary_key=True),
    Column("id_contrato", Integer, nullable=False, primary_key=True),
    Column("id_cliente", Integer, nullable=False, primary_key=True),
    CheckConstraint(
        """typeof(id_contrato) = "integer" & id_contrato >= 0
    & typeof(id_cliente) = "integer" & id_cliente >= 0
    & typeof(id_pago) = "integer" & id_pago >= 0
    & typeof(monto) = "float" & monto > 0""",
        name="is a natural number",
    ),
    Column("fecha", DateTime, nullable=False, primary_key=True),
    Column("monto", Float, nullable=False, primary_key=True),
    Column("fecha_registro", DateTime, nullable=False),
    Column("activo", Boolean, nullable=False, primary_key=True),
).create(engine)
