# ohtuvarasto
Ohjelmistotuotannon tehtävä kansio


[![GHA workflow badge](https://github.com/Grelod-bit/ohtuvarasto/actions/workflows/main.yml/badge.svg)](https://github.com/Grelod-bit/ohtuvarasto/actions)
[![codecov](https://codecov.io/github/Grelod-bit/ohtuvarasto/graph/badge.svg?token=8E6MHV5E0D)](https://codecov.io/github/Grelod-bit/ohtuvarasto)

## Web interface

Install the project dependencies with `uv sync`, then start the warehouse web
interface with `uv run python src/web.py`. Open http://127.0.0.1:5000 to create
items and manage their in-memory stock. Inventory is cleared when the server
stops.
