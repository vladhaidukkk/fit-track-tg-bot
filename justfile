default: fmt fix

# Startup Commands
compose_file := "docker-compose-local.yaml"

run:
    python -m bot.main

up:
    docker compose -f {{compose_file}} up -d

down:
    docker compose -f {{compose_file}} down

# Code Styling
fmt:
    ruff format
    taplo format

lint:
    ruff check

fix:
    ruff check --fix
