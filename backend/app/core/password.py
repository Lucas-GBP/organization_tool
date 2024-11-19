import bcrypt

def hash_password(password: str) -> str:
    # Gerar um sal (salt) e fazer o hash da senha
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')  # Retorna como string para salvar no banco

def verify_password(password: str, hashed_password: str) -> bool:
    # Verificar a senha usando bcrypt
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))