import bcrypt

def hash_password(password: str) -> str:
    """
    对密码进行哈希处理
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()
   
def verify_password(password: str, hashed_password: str) -> bool:
    """
    验证密码是否匹配
    """
    return bcrypt.checkpw(password.encode(), hashed_password.encode()) 