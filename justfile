default: fmt fix

fmt:
    ruff format
    taplo format

lint:
    ruff check

fix:
    ruff check --fix
