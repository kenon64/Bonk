"""
Точка входа для запуска Bonk как модуля.

Позволяет запускать программу командой:
    python -m bonk
"""

from .cli import cli

if __name__ == "__main__":
    cli()
