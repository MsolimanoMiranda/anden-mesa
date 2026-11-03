from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Mesa:
    id: str
    nombre: str
    capacidad: int
    zona: str


@dataclass(frozen=True)
class Reserva:
    id: str
    mesa_id: str
    titular: str
    comensales: int
    inicio: datetime
    fin: datetime
    activa: bool = True

    def se_cruza_con(self, inicio: datetime, fin: datetime) -> bool:
        if not self.activa:
            return False
        return self.inicio < fin and inicio < self.fin
