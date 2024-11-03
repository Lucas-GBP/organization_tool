#!/bin/sh

# Entra na pasta pai do projeto
cd ..
# Executa o mypy com os argumentos desejados
poetry run mypy . --allow-redefinition --show-error-codes --pretty --explicit-package-bases