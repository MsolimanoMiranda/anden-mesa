import os

import uvicorn

from mesa.adapters.api import crear_app
from mesa.adapters.sqlite import SqliteMesas, SqliteReservas, conectar
from mesa.application.reservar import LibroDeReservas


def construir():
    ruta = os.environ.get("MESA_DB", "data/mesa.db")
    cx = conectar(ruta)
    return crear_app(LibroDeReservas(SqliteMesas(cx), SqliteReservas(cx)))


app = construir()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "3043")))
