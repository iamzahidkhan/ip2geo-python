import requests


class Ip2Geo:
    BASE_URL = "https://api.ip2geoapi.com/ip"

    def __init__(self, api_key: str | None = None, timeout: int = 10):
        self.api_key = api_key
        self.timeout = timeout

    def lookup(
        self,
        ip: str | None = None,
        format: str | None = None,
        callback: str | None = None,
    ):
        params = {}

        # API key (optional, API handles missing key response)
        if self.api_key:
            params["key"] = self.api_key

        # format is optional (defaults to JSON if not provided)
        if format:
            params["format"] = format

        # callback only valid for jsonp
        if callback:
            if format != "jsonp":
                raise ValueError("callback can only be used when format='jsonp'")
            params["callback"] = callback

        url = f"{self.BASE_URL}/{ip}" if ip else self.BASE_URL

        response = requests.get(url, params=params, timeout=self.timeout)

        # HTTP-level error (network / server)
        if not response.ok:
            raise RuntimeError(
                f"Ip2Geo API error {response.status_code}: {response.text}"
            )

        # JSON response handling
        if format in (None, "json"):
            data = response.json()

            if not data.get("success", False):
                # API-level error (eg: missing API key)
                raise RuntimeError(data.get("error", "Unknown API error"))

            return data

        # Non-JSON formats return raw text
        return response.text
