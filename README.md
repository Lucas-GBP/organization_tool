# Organization Tool

## Database

### Atualizando o banco de dados
```bash
docker-compose exec backend bash
poetry shell
alembic revision --autogenerate -m "comment"
alembic upgrade head
```


## Backend

### Poetry and Vscode config
With vscode closed execute the following command:

```bash
cd backend

poetry install

poetry run code ../
```
#### Extensions optional
Install MyPy by Matan Grover as a vscode extension.
```bash
poetry env info
```
copy the Path parameter. In the vscode settings Mypy: Dmypy Executable put "{Path}/bin/dmypy" and in Mypy: Targets only informe one path "./backend"

## Frontend
