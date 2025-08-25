import os, httpx
FMP_KEY = os.getenv("FMP_API_KEY")
BASE = "https://financialmodelingprep.com/api/v3"
async def get(path: str, params: dict | None = None):
    p = {"apikey": FMP_KEY, **(params or {})}
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(f"{BASE}/{path}", params=p)
        r.raise_for_status(); return r.json()
