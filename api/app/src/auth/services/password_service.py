import bcrypt


def encrypt_password(input_password):
    return bcrypt.hashpw(input_password.encode(), bcrypt.gensalt())


def check_password(input_password, hashed_password):
    return bcrypt.checkpw(input_password.encode(), hashed_password)
