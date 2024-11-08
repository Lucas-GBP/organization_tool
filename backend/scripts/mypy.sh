#!/bin/sh
# Executa o mypy com os argumentos desejados
echo "Running mypy in poetry enviroment..."
poetry run mypy . --allow-redefinition --show-error-codes --pretty --explicit-package-bases