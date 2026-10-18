from unittest.mock import AsyncMock, MagicMock, patch

def test_get_tables_list(client):
    mock_redis = MagicMock()
    mock_redis.get = AsyncMock(return_value=None)
    mock_redis.set = AsyncMock(return_value=True)

    with patch("app.routers.tables.redis_client", mock_redis):
        response = client.get("/tables")
        assert response.status_code == 200
        assert isinstance(response.json(), list)