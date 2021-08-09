from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.PagoModel import Pago
from src.config import engine


def test_new_registry_between_fecha_range_clone_and_disable_highers_than_new():
    PAGOS_TO_INSERT = [
        Pago(id_contrato=12, id_cliente=99, fecha=datetime(2021, 8, 5), monto=7000),
        Pago(id_contrato=12, id_cliente=99, fecha=datetime(2021, 8, 6), monto=1280),
        Pago(id_contrato=12, id_cliente=99, fecha=datetime(2021, 8, 7), monto=4900),
    ]
    print(f"adding {len(PAGOS_TO_INSERT)} registries at latest date")
    with Session(engine) as session:
        for _pago in PAGOS_TO_INSERT:
            Pago.add_registry(session, _pago)
            session.commit()

        table = (
            session.execute(select(Pago).order_by(Pago.activo, Pago.id_pago))
            .scalars()

        )
        for row in table.all():
            print(row)
        assert len(table) == 3

    print("adding one registry in between range of fecha")
    with Session(engine) as session:
        second_registry = Pago(
            id_contrato=12, id_cliente=99, fecha=datetime(2021, 8, 4), monto=900
        )
        Pago.add_registry(session, second_registry)
        session.commit()

        # show full table
        table = (
            session.execute(select(Pago).order_by(Pago.activo, Pago.id_pago))
            .scalars()
        )
        for row in table.all():
            print(row)
        assert len(table) == 7
