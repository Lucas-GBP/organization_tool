from typing import Any
from sqlalchemy import Select
from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger
from alembic_utils.pg_view import PGView

from .base import Base, BaseView

#
# Basic entities
#
def view_entity(
    tabelView:str|type[BaseView], 
    statement:Select[Any]|str,
    schema:str = "public"
) -> PGView:
    """
    Esta função cria uma visualização em PostgreSQL a partir de uma tabela e um statement SQL.

    Argumentos:
    - tabelView (BaseView): Um objeto que representa a tabela base para a qual a visualização será criada.
    - statement (Select | str): Um statement SQL, que pode ser um objeto SQLAlchemy `Select` ou uma string. 
      Se for um objeto `Select`, ele será convertido para string, e certos padrões relacionados ao nome da tabela serão removidos da query. 
      Se for uma string, ela será usada diretamente sem modificações.

    Retorno:
    - PGView: Um objeto que representa a visualização PostgreSQL, contendo o esquema, assinatura e definição da visualização.
    """
    if isinstance(tabelView, str):
        table_name = tabelView
    else:
        table_name = str(tabelView.__tablename__)
    
    if isinstance(statement, str):
        definition = statement
    else:
        definition = str(statement).replace(table_name+".", "").replace(", "+table_name, "")

    return PGView(
        schema=schema,
        signature=table_name,
        definition=definition,
    )

def trigger_entity(
    signature:str,
    on_entity:str|type[Base],
    definition:str,
    schema:str = "public",
    is_constraint:bool = False
) -> PGTrigger:
    if isinstance(on_entity, str):
        entity_name = on_entity
    else:
        entity_name = str(on_entity.__tablename__)
        
    return PGTrigger(
        signature=signature,
        definition=definition,
        on_entity=entity_name,
        schema=schema,
        is_constraint=is_constraint
    )

def function_entity(
    signature:str,
    definition:str,
    schema:str = "public"
) -> PGFunction:
    definition_formated = definition

    return PGFunction(
        signature=signature,
        definition=definition_formated,
        schema=schema
    )