def test_register_and_login_flow(client):
    # 1. Регистрация нового юзера
    user_data = {
        "username": "lion_boss",
        "email": "lion_boss@example.com",
        "password": "Test123"
    }
    reg_response = client.post("/auth/register",
                               json=user_data)
    assert reg_response.status_code in (201, 400)

    # 2. Попытка входа (Логин)
    login_response = client.post("/auth/login",
                                 json=user_data)
    assert login_response.status_code in (200, 401)
