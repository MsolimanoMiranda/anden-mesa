from mesa.domain.modelos import Mesa, Reserva


class MesasEnMemoria:
    def __init__(self) -> None:
        self._mesas: dict[str, Mesa] = {}

    def guardar(self, mesa: Mesa) -> None:
        self._mesas[mesa.id] = mesa

    def obtener(self, mesa_id: str) -> Mesa | None:
        return self._mesas.get(mesa_id)

    def listar(self) -> list[Mesa]:
        return list(self._mesas.values())


class ReservasEnMemoria:
    def __init__(self) -> None:
        self._reservas: dict[str, Reserva] = {}

    def guardar(self, reserva: Reserva) -> None:
        self._reservas[reserva.id] = reserva

    def obtener(self, reserva_id: str) -> Reserva | None:
        return self._reservas.get(reserva_id)

    def de_mesa(self, mesa_id: str) -> list[Reserva]:
        return [r for r in self._reservas.values() if r.mesa_id == mesa_id]

    def listar_activas(self) -> list[Reserva]:
        return [r for r in self._reservas.values() if r.activa]
