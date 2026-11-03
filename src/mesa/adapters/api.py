from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from mesa.application.reservar import LibroDeReservas
from mesa.domain.errores import NoEncontrado, ReglaDeNegocio
from mesa.domain.modelos import Mesa, Reserva


class MesaIn(BaseModel):
    nombre: str
    capacidad: int
    zona: str = "salón"


class ReservaIn(BaseModel):
    mesa_id: str
    titular: str
    comensales: int
    inicio: datetime
    fin: datetime


def crear_app(libro: LibroDeReservas) -> FastAPI:
    app = FastAPI(title="Mesa lista", version="1.0.0")

    @app.get("/salud")
    def salud() -> dict[str, str]:
        return {"servicio": "mesa-lista"}

    @app.post("/mesas", status_code=201)
    def abrir_mesa(body: MesaIn) -> dict:
        try:
            return _mesa(libro.abrir_mesa(body.nombre, body.capacidad, body.zona))
        except ReglaDeNegocio as exc:
            raise HTTPException(422, str(exc)) from exc

    @app.get("/mesas")
    def listar_mesas() -> list[dict]:
        return [_mesa(mesa) for mesa in libro.listar_mesas()]

    @app.post("/reservas", status_code=201)
    def reservar(body: ReservaIn) -> dict:
        try:
            reserva = libro.reservar(body.mesa_id, body.titular, body.comensales, body.inicio, body.fin)
        except NoEncontrado as exc:
            raise HTTPException(404, str(exc)) from exc
        except ReglaDeNegocio as exc:
            raise HTTPException(422, str(exc)) from exc
        return _reserva(reserva)

    @app.post("/reservas/{reserva_id}/cancelar")
    def cancelar(reserva_id: str) -> dict:
        try:
            return _reserva(libro.cancelar(reserva_id))
        except NoEncontrado as exc:
            raise HTTPException(404, str(exc)) from exc
        except ReglaDeNegocio as exc:
            raise HTTPException(422, str(exc)) from exc

    @app.get("/reservas")
    def activas() -> list[dict]:
        return [_reserva(reserva) for reserva in libro.listar_activas()]

    return app


def _mesa(mesa: Mesa) -> dict:
    return {"id": mesa.id, "nombre": mesa.nombre, "capacidad": mesa.capacidad, "zona": mesa.zona}


def _reserva(reserva: Reserva) -> dict:
    return {
        "id": reserva.id,
        "mesaId": reserva.mesa_id,
        "titular": reserva.titular,
        "comensales": reserva.comensales,
        "inicio": reserva.inicio.isoformat(),
        "fin": reserva.fin.isoformat(),
        "activa": reserva.activa,
    }
