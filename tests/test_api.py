from fastapi.testclient import TestClient

from mesa.adapters.api import crear_app
from mesa.adapters.sqlite import SqliteMesas, SqliteReservas, conectar
from mesa.application.reservar import LibroDeReservas


def test_reservar_por_http(tmp_path):
    cx = conectar(str(tmp_path / "mesa.db"))
    app = crear_app(LibroDeReservas(SqliteMesas(cx), SqliteReservas(cx)))
    client = TestClient(app)

    mesa = client.post("/mesas", json={"nombre": "Patio", "capacidad": 4, "zona": "aire"}).json()
    reserva = client.post(
        "/reservas",
        json={
            "mesa_id": mesa["id"],
            "titular": "Nora",
            "comensales": 4,
            "inicio": "2026-11-02T19:00:00",
            "fin": "2026-11-02T21:00:00",
        },
    )
    assert reserva.status_code == 201
    cruce = client.post(
        "/reservas",
        json={
            "mesa_id": mesa["id"],
            "titular": "Omar",
            "comensales": 2,
            "inicio": "2026-11-02T20:00:00",
            "fin": "2026-11-02T22:00:00",
        },
    )
    assert cruce.status_code == 422
    assert client.get("/reservas").json()[0]["titular"] == "Nora"
