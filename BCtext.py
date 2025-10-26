import bcrypt

password = "driver123"
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print(hashed.decode())
