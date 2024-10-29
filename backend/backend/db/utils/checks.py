from sqlalchemy import CheckConstraint

def CheckColorHex(column_name:str, nullable:bool = True):
    checkName = "check_color_hex"
    if nullable:
        return CheckConstraint(
            f"({column_name} IS NULL OR {column_name}"+r" ~* '^#[a-f0-9]{6}$')",
            name=checkName
        )
    else:
        return CheckConstraint(
            "("+column_name+r" ~* '^#[a-f0-9]{6}$')",
            name=checkName
        )