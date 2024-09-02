from sqlalchemy import CheckConstraint
from sqlalchemy.orm import MappedColumn

def CheckColorHex(column:str|MappedColumn, nullable:bool = True):
    STRING_COLOR_FORMAT = r" ~* '^#[a-f0-9]{6}$')"
    if isinstance(column, str):
        column_name = column
    else:
        column_name = str(column.name)

    if nullable:
        constrain = f"({column_name} IS NULL OR {column_name}" + STRING_COLOR_FORMAT
    else:
        constrain = f"({column_name}" + STRING_COLOR_FORMAT
    
    return CheckConstraint(
        constrain,
        name="check_color_hex"
    )