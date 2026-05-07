import httpx


class ApiClient:
    def __init__(self, base_url: str, api_token: str):
        self._api_token = api_token
        self._client = httpx.Client(base_url=base_url, timeout=30.0)
        self._jwt: str | None = None

    def _authenticate(self) -> None:
        if self._jwt:
            return
        response = self._client.post("/api/login", json={"api_token": self._api_token})
        response.raise_for_status()
        self._jwt = response.json()["jwt"]
        self._client.headers["Authorization"] = self._jwt

    def get(self, path: str, **kwargs) -> httpx.Response:
        self._authenticate()
        return self._client.get(path, **kwargs)

    def post(self, path: str, **kwargs) -> httpx.Response:
        self._authenticate()
        return self._client.post(path, **kwargs)

    def close(self) -> None:
        self._client.close()
