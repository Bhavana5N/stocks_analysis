from fastapi import APIRouter, HTTPException
from ..services.db import get_conn
from ..services.fmp import get as fmp_get
import datetime as dt

router = APIRouter()

@router.get("/prices/{symbol}")
async def prices(symbol: str, days: int = 200):
    data = await fmp_get(f"historical-price-full/{symbol.upper()}", {"serietype":"line","timeseries":days})
    hist = data.get("historical", [])
    if not hist: raise HTTPException(404, "No data")
    conn = await get_conn()
    try:
        await conn.executemany(
            """INSERT INTO prices(symbol, ts, o,h,l,c,v, interval)
                 VALUES($1,$2,$3,$4,$5,$6,$7,'1d')
                 ON CONFLICT (symbol, ts, interval) DO UPDATE
                 SET o=EXCLUDED.o, h=EXCLUDED.h, l=EXCLUDED.l, c=EXCLUDED.c, v=EXCLUDED.v""",
            [(
              symbol.upper(), dt.datetime.fromisoformat(p["date"]+"T00:00:00"),
              p["open"], p["high"], p["low"], p["close"], p["volume"]
            ) for p in hist]
        )
    finally:
        await conn.close()
    return {"rows": len(hist)}
