# Mesa lista

Reservas de restaurante en FastAPI con arquitectura hexagonal. El dominio decide si dos reservas se cruzan; SQLite solo guarda.

## Capas

- `domain` — `Mesa`, `Reserva` y la regla de solape.
- `application` — abrir mesa, reservar, cancelar.
- `ports` — protocolos de repositorio.
- `adapters` — memoria (pruebas), SQLite y FastAPI.

## Correr

```bash
cd projects/fastapi-mesa
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pytest
PYTHONPATH=src python -m mesa.main
```

El API escucha en el puerto `3043`. `POST /mesas` y `POST /reservas`.
