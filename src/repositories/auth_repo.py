class AuthRepo:
    async def get_by_login(self, username: str):
        # Временно — мок-данные
        if username == "admin":
            return type("Employee", (), {"username": "admin", "password": "1234"})
        return None
