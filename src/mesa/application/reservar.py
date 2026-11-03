from datetime import datetime
from uuid import uuid4

from mesa.domain.errores import NoEncontrado, ReglaDeNegocio
from mesa.domain.modelos import Mesa, Reserva
from mesa.ports.repositorios import MesaRepositorio, ReservaRepositorio


class LibroDeReservas:
    def __init__(self, mesas: MesaRepositorio, reservas: ReservaRepositorio) -> None:
        self._mesas = mesas
        self._reservas = reservas

    def abrir_mesa(self, nombre: str, capacidad: int, zona: str) -> Mesa:
        if not nombre.strip():
            raise ReglaDeNegocio("La mesa necesita un nombre")
        if capacidad < 1:
            raise ReglaDeNegocio("La capacidad debe ser al menos 1")
        mesa = Mesa(id=str(uuid4()), nombre=nombre.strip(), capacidad=capacidad, zona=zona.strip() or "salón")
        self._mesas.guardar(mesa)
        return mesa

    def reservar(
        self,
        mesa_id: str,
        titular: str,
        comensales: int,
        inicio: datetime,
        fin: datetime,
    ) -> Reserva:
        mesa = self._mesas.obtener(mesa_id)
        if mesa is None:
            raise NoEncontrado("Mesa no encontrada")
        if not titular.strip():
            raise ReglaDeNegocio("La reserva necesita un titular")
        if comensales < 1:
            raise ReglaDeNegocio("Tiene que venir al menos una persona")
        if comensales > mesa.capacidad:
            raise ReglaDeNegocio(f"La mesa {mesa.nombre} admite {mesa.capacidad}")
        if fin <= inicio:
            raise ReglaDeNegocio("La reserva termina antes de empezar")
        for existente in self._reservas.de_mesa(mesa_id):
            if existente.se_cruza_con(inicio, fin):
                raise ReglaDeNegocio("Esa mesa ya está reservada en ese horario")
        reserva = Reserva(
            id=str(uuid4()),
            mesa_id=mesa_id,
            titular=titular.strip(),
            comensales=comensales,
            inicio=inicio,
            fin=fin,
        )
        self._reservas.guardar(reserva)
        return reserva

    def listar_mesas(self) -> list[Mesa]:
        return self._mesas.listar()

    def listar_activas(self) -> list[Reserva]:
        return self._reservas.listar_activas()

    def cancelar(self, reserva_id: str) -> Reserva:
        reserva = self._reservas.obtener(reserva_id)
        if reserva is None:
            raise NoEncontrado("Reserva no encontrada")
        if not reserva.activa:
            raise ReglaDeNegocio("La reserva ya estaba cancelada")
        cancelada = Reserva(
            id=reserva.id,
            mesa_id=reserva.mesa_id,
            titular=reserva.titular,
            comensales=reserva.comensales,
            inicio=reserva.inicio,
            fin=reserva.fin,
            activa=False,
        )
        self._reservas.guardar(cancelada)
        return cancelada
