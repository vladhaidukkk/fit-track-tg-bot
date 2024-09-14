default: fmt fix

# Startup Commands
run:
    python -m bot.main

# Code Styling
fmt:
    ruff format
    taplo format

lint:
    ruff check

fix:
    ruff check --fix
