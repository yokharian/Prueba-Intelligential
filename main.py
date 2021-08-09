from datetime import datetime

import click


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
    print(id_contrato, id_cliente, monto, fecha)


if __name__ == "__main__":
    registrar_pago()
