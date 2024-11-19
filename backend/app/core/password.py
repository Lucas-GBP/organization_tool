from bcrypt import gensalt, hashpw, checkpw

ENCODE = 'utf-8'

def hash_password(password: str) -> str:
    # Gerar um sal (salt) e fazer o hash da senha
    salt = gensalt()
    hashed_password = hashpw(password.encode(ENCODE), salt)
    return hashed_password.decode(ENCODE)  # Retorna como string para salvar no banco

def verify_password(password: str, hashed_password: str) -> bool:
    # Verificar a senha usando bcrypt
    return checkpw(password.encode(ENCODE), hashed_password.encode(ENCODE))