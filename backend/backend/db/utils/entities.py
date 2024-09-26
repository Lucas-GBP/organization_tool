from sqlalchemy import Select
from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger
from alembic_utils.pg_view import PGView

from .base import Base, BaseView

def view_entity(tabelView:BaseView, statement:Select|str):
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
    table_name = str(tabelView.__tablename__)
    if isinstance(statement, str):
        query = statement
    else:
        query = str(statement).replace(table_name+".", "").replace(", "+table_name, "").replace(table_name+", ", "")

    return PGView(
        schema="public",
        signature=table_name,
        definition=query,
    )

def trigger_entity(
    signature:str,
    definition:str,
    on_entity:str|Base,
    schema:str = "public",
    is_constrain:bool = False
):
    if isinstance(on_entity, str):
        entity_name = on_entity
    else:
        entity_name = str(on_entity.__tablename__)
        
    return PGTrigger(
        signature=signature,
        definition=definition,
        on_entity=entity_name,
        schema=schema,
        is_constraint=is_constrain
    )

def function_entity(
    signature:str,
    definition:str,
    schema:str = "public"
):
    return PGFunction(
        signature=signature,
        definition=definition,
        schema=schema
    )