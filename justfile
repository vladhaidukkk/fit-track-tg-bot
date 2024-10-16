default: fmt fix

# Dependencies Management Commands
reqs:
    poetry export -f requirements.txt --output requirements.txt --without-hashes

# Startup Commands
compose_file := "docker-compose-local.yaml"

run:
    python -m bot.main

debug:
    PYTHONBREAKPOINT=ipdb.set_trace python -m bot.main

up:
    docker compose -f {{compose_file}} up -d

down:
    docker compose -f {{compose_file}} down

# Code Styling Commands
fmt:
    ruff format
    taplo format

lint:
    ruff check

fix:
    ruff check --fix

# Testing Commands
test:
    python -m pytest

# Migrations Management Commands
revise msg:
    alembic revision --autogenerate -m "{{msg}}"

migrate target="head":
    alembic upgrade {{target}}

revert target="-1":
    alembic downgrade {{target}}
