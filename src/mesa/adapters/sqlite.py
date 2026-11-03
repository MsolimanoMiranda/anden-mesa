import sqlite3
from datetime import datetime
from pathlib import Path

from mesa.domain.modelos import Mesa, Reserva


_SCHEMA = """
CREATE TABLE IF NOT EXISTS mesa (
    id TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    capacidad INTEGER NOT NULL,
    zona TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS reserva (
    id TEXT PRIMARY KEY,
    mesa_id TEXT NOT NULL,
    titular TEXT NOT NULL,
    comensales INTEGER NOT NULL,
    inicio TEXT NOT NULL,
    fin TEXT NOT NULL,
    activa INTEGER NOT NULL
);
"""


class SqliteMesas:
    def __init__(self, conexion: sqlite3.Connection) -> None:
        self._cx = conexion

    def guardar(self, mesa: Mesa) -> None:
        self._cx.execute(
            """
            INSERT INTO mesa (id, nombre, capacidad, zona) VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET nombre = excluded.nombre,
                capacidad = excluded.capacidad, zona = excluded.zona
            """,
            (mesa.id, mesa.nombre, mesa.capacidad, mesa.zona),
        )
        self._cx.commit()

    def obtener(self, mesa_id: str) -> Mesa | None:
        fila = self._cx.execute("SELECT id, nombre, capacidad, zona FROM mesa WHERE id = ?", (mesa_id,)).fetchone()
        if fila is None:
            return None
        return Mesa(*fila)

    def listar(self) -> list[Mesa]:
        filas = self._cx.execute("SELECT id, nombre, capacidad, zona FROM mesa ORDER BY nombre").fetchall()
        return [Mesa(*fila) for fila in filas]


class SqliteReservas:
    def __init__(self, conexion: sqlite3.Connection) -> None:
        self._cx = conexion

    def guardar(self, reserva: Reserva) -> None:
        self._cx.execute(
            """
            INSERT INTO reserva (id, mesa_id, titular, comensales, inicio, fin, activa)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET activa = excluded.activa
            """,
            (
                reserva.id,
                reserva.mesa_id,
                reserva.titular,
                reserva.comensales,
                reserva.inicio.isoformat(),
                reserva.fin.isoformat(),
                1 if reserva.activa else 0,
            ),
        )
        self._cx.commit()

    def obtener(self, reserva_id: str) -> Reserva | None:
        fila = self._cx.execute(
            "SELECT id, mesa_id, titular, comensales, inicio, fin, activa FROM reserva WHERE id = ?",
            (reserva_id,),
        ).fetchone()
        return None if fila is None else self._fila(fila)

    def de_mesa(self, mesa_id: str) -> list[Reserva]:
        filas = self._cx.execute(
            "SELECT id, mesa_id, titular, comensales, inicio, fin, activa FROM reserva WHERE mesa_id = ?",
            (mesa_id,),
        ).fetchall()
        return [self._fila(fila) for fila in filas]

    def listar_activas(self) -> list[Reserva]:
        filas = self._cx.execute(
            "SELECT id, mesa_id, titular, comensales, inicio, fin, activa FROM reserva WHERE activa = 1"
        ).fetchall()
        return [self._fila(fila) for fila in filas]

    @staticmethod
    def _fila(fila: tuple) -> Reserva:
        return Reserva(
            id=fila[0],
            mesa_id=fila[1],
            titular=fila[2],
            comensales=fila[3],
            inicio=datetime.fromisoformat(fila[4]),
            fin=datetime.fromisoformat(fila[5]),
            activa=bool(fila[6]),
        )


def conectar(ruta: str) -> sqlite3.Connection:
    if ruta != ":memory:":
        Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    cx = sqlite3.connect(ruta, check_same_thread=False)
    cx.executescript(_SCHEMA)
    return cx
