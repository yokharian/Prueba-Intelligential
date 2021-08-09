import pytest

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from PagoModel import Pago
from config import engine

if __name__ == "__main__":
    PAGOS_TO_INSERT = [
        Pago(id_contrato=12, id_cliente=99, fecha=datetime(2021, 8, 5), monto=7000),
        Pago(id_contrato=12, id_cliente=99, fecha=datetime(2021, 8, 6), monto=1280),
        Pago(id_contrato=12, id_cliente=99, fecha=datetime(2021, 8, 7), monto=4900),
    ]

    with Session(engine) as session:
        for _pago in PAGOS_TO_INSERT:
            Pago.add_registry(session, _pago)
            session.commit()
        table = list(session.execute(select(Pago)).scalars())
        for row in table:
            print(row)

    print('adding one')

    with Session(engine) as session:
        Pago.add_registry(session, Pago(id_contrato=12, id_cliente=99, fecha=datetime(2021, 8, 4), monto=900))
        session.commit()

        table = list(session.execute(select(Pago).order_by(Pago.activo,Pago.id_pago)).scalars())
        for row in table:
            print(row)
