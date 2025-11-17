class AuthRepo:
    async def get_by_login(self, username: str):
        if username == "admin":
            return type("Employee", (), {"username": "admin", "password": "1234"})
        return None
