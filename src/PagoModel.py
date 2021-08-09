"""define ORM functionality"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Float,
    Boolean,
    select,
    desc,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import Select

from .config import DATE_FORMAT

Base = declarative_base()


class Pago(Base):
    __tablename__: str = "PAGO"

    # Identificador del pago
    id_pago = Column(Integer, primary_key=True)

    id_contrato = Column(Integer, nullable=False, primary_key=True)  # Identificador del contrato
    id_cliente = Column(Integer, nullable=False, primary_key=True)  # Identificador del cliente
    fecha = Column(DateTime, nullable=False, primary_key=True)  # Fecha de pago
    monto = Column(Float, nullable=False, primary_key=True)  # Monto del pago
    # true si el registro está vigente, false si el registro ya no es válido (eliminado lógico)
    activo = Column(Boolean, primary_key=True, default=True)
    fecha_registro = Column(DateTime, default=datetime.now())  # Fecha de registro del pago

    @classmethod
    def select_latest_pagos(
        cls, id_contrato: int, id_cliente: int, activo=True
    ) -> Select:
        return (
            select(cls)
            .where(
                cls.id_contrato == id_contrato,
                cls.id_cliente == id_cliente,
                cls.activo == activo,
            )
            .order_by(desc(cls.fecha))
        )

    def get_consecutive_pagos(self) -> Select:
        cls = type(self)
        return select(cls).where(
            cls.fecha >= self.fecha,
            cls.id_contrato == self.id_contrato,
            cls.activo == True,
        )

    def clone(self):
        table = self.__table__
        data = {c: getattr(self, c) for c in table.columns.keys()}
        data.update(activo=False)
        clone = self.__class__(**data)
        return clone

    def recalculate_consecutive_ids(self, _session) -> Pago:
        """replace consecutive ids found, i.e rows with (id_pago > starting_id_pago)"""
        # consecutive pagos
        SELECT_STM = self.get_consecutive_pagos()
        # TODO develop chunk iteration strategy in the future (to avoid high ram usage)

        # disable original rows
        original_rows = _session.execute(SELECT_STM).scalars().all()
        for row in original_rows:
            row.activo = False

        # duplicate original rows with recalculated id
        for cloned_row in (row.clone() for row in original_rows):
            self.id_pago = cloned_row.id_pago if self.id_pago is None else self.id_pago
            cloned_row.id_pago += 1
            cloned_row.activo = True
            _session.add(cloned_row)

    @classmethod
    def add_registry(cls, _session, pago_to_add):
        """related logic for specific constraint and business logic

        05 august 2021.- Se pueden recibir pagos con fechas anteriores a los pagos ya registrados
        de un contrato, es decir, si ya existen N pagos con fechas F0,...,FN
        en la tabla de pagos y se recibe un pago con fecha F' donde
        F' < {Fk,...,Fm} (F' es anterior a 1 o varios pagos de un contrato),
        se desactivarán todos los pagos del contrato posteriores a F',
        se insertará el nuevo pago con fecha F' y se insertarán nuevos registros
        para los pagos que ya existían (posteriores a F'), de tal manera que
        para todos los pagos de un mismo contrato si Fi < Fj
        entonces id_pago[i] < id_pago[j]
        """
        STARTING_ID_PAGO = 1
        LATEST_PAGO_STM = cls.select_latest_pagos(
            id_contrato=pago_to_add.id_contrato, id_cliente=pago_to_add.id_cliente
        ).limit(1)
        # https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Result.scalars
        latest_pago: Optional[cls] = _session.execute(LATEST_PAGO_STM).scalar()

        # autoincrement id_pago functionality
        # as sqlite doesn't support autoincrement with composed primary keys
        if latest_pago is None:
            pago_to_add.id_pago = STARTING_ID_PAGO
        elif pago_to_add.fecha > latest_pago.fecha:  # pago_to_add has maximum fecha
            pago_to_add.id_pago = latest_pago.id_pago + 1
        else:  # pago between (min and max) fecha range
            pago_to_add.recalculate_consecutive_ids(_session)
        _session.add(pago_to_add)

    def __repr__(self):
        id_pago, fecha, id_contrato, monto, activo = (
            self.id_pago,
            self.fecha.strftime(DATE_FORMAT),
            self.id_contrato,
            self.monto,
            self.activo,
        )
        return f"Pago con {id_pago=}, {fecha=}, {id_contrato=}, {monto=}, {activo=}"
