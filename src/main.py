from datetime import datetime

import click

from PagoModel import Pago
from build_database import fully_build_database
from config import engine
from dags import dag_add_pago


@click.group(chain=True)
def cli():
    pass


@cli.command('add_pago')
@click.option("--id_contrato", required=True, type=int)
@click.option("--id_cliente", required=True, type=int)
@click.option("--monto", "--cantidad", required=True, type=int)
@click.option(
    "--echo", type=bool, default=True, help="show table (before & after) result"
)
@click.option(
    "--fecha",
    required=True,
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="fecha de pago",
)
def cli_dag_add_pago(
    id_contrato: int,
    id_cliente: int,
    monto: int,
    fecha: datetime,
    echo,
):
    new_registry = Pago(
        id_contrato=id_contrato, id_cliente=id_cliente, monto=monto, fecha=fecha
    )
    dag_add_pago(new_registry, echo)


@cli.command('build_database')
def bdist_wheel():
    fully_build_database(engine)
    print('database created successfully !!!!')


if __name__ == '__main__':
    cli()
