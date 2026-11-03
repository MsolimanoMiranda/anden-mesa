from datetime import datetime

import pytest

from mesa.adapters.memoria import MesasEnMemoria, ReservasEnMemoria
from mesa.application.reservar import LibroDeReservas
from mesa.domain.errores import ReglaDeNegocio


def libro() -> LibroDeReservas:
    return LibroDeReservas(MesasEnMemoria(), ReservasEnMemoria())


def test_no_permite_solape_y_libera_al_cancelar():
    svc = libro()
    mesa = svc.abrir_mesa("Ventana", 4, "salón")
    inicio = datetime(2026, 11, 2, 13, 0)
    fin = datetime(2026, 11, 2, 15, 0)
    reserva = svc.reservar(mesa.id, "Ana", 2, inicio, fin)
    with pytest.raises(ReglaDeNegocio):
        svc.reservar(mesa.id, "Luis", 2, datetime(2026, 11, 2, 14, 0), datetime(2026, 11, 2, 16, 0))
    svc.cancelar(reserva.id)
    otra = svc.reservar(mesa.id, "Luis", 2, datetime(2026, 11, 2, 14, 0), datetime(2026, 11, 2, 16, 0))
    assert otra.activa


def test_rechaza_mas_comensales_que_la_capacidad():
    svc = libro()
    mesa = svc.abrir_mesa("Barra", 2, "barra")
    with pytest.raises(ReglaDeNegocio):
        svc.reservar(
            mesa.id,
            "Ana",
            3,
            datetime(2026, 11, 2, 20, 0),
            datetime(2026, 11, 2, 21, 0),
        )
