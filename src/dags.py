from sqlalchemy.orm import Session

from PagoModel import Pago
from config import engine


def dag_add_pago(new_registry: Pago, echo=True):
    with Session(engine) as session:
        if echo:
            print("-- before --")
            for row in session.query(Pago).all():
                print(row)

        Pago.add_registry(session, new_registry)
        session.commit()

        if echo:
            print("\n-- after --")
            for row in session.query(Pago).all():
                print(row)