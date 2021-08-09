from datetime import datetime

import click
from sqlalchemy.orm import Session

from src.PagoModel import Pago
from src.config import engine


def dag_add_pago(id_contrato: int, id_cliente: int, monto: int, fecha: datetime):
    new_registry = Pago(
        id_contrato=id_contrato, id_cliente=id_cliente, monto=monto, fecha=fecha
    )
    with Session(engine) as session:
        Pago.add_registry(session, new_registry)
        session.commit()


@click.command()
@click.option("--id_contrato", required=True, type=int)
@click.option("--id_cliente", required=True, type=int)
@click.option("--monto", "--cantidad", required=True, type=int)
@click.option(
    "--fecha",
    required=True,
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="fecha de pago",
)
def registrar_pago(id_contrato: int, id_cliente: int, monto: int, fecha: datetime):
    dag_add_pago(
        id_contrato=id_contrato, id_cliente=id_cliente, monto=monto, fecha=fecha
    )


if __name__ == "__main__":
    registrar_pago()
