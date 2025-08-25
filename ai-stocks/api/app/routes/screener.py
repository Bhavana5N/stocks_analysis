from fastapi import APIRouter, Query
from ..services.db import get_conn

router = APIRouter()

@router.get("/screener")
async def screener(
    value_pe_lt: float | None = Query(None),
    value_peg_lt: float | None = Query(None),
    squeeze_on: bool | None = Query(None),
    squeeze_firing: bool | None = Query(None),
    breakout: bool | None = Query(None),
    near_breakout: bool | None = Query(None),
    limit: int = 50,
):
    where = ["1=1"]; params = []
    def add(sql, val): params.append(val); where.append(sql)
    if value_pe_lt is not None:  add(f"t.pe < ${len(params)+1}", value_pe_lt)
    if value_peg_lt is not None: add(f"t.peg < ${len(params)+1}", value_peg_lt)
    if squeeze_on is not None:   add(f"i.squeeze_on = ${len(params)+1}", squeeze_on)
    if squeeze_firing is not None: add(f"i.squeeze_firing = ${len(params)+1}", squeeze_firing)
    if breakout is not None:     add(f"i.breakout_55d = ${len(params)+1}", breakout)
    if near_breakout is not None:add(f"i.near_breakout = ${len(params)+1}", near_breakout)

    q = f"""
    SELECT t.symbol, t.name, t.sector, t.pe, t.peg, i.squeeze_on, i.squeeze_firing,
           i.breakout_55d, i.near_breakout
    FROM tickers t
    JOIN LATERAL (
      SELECT * FROM indicators i2 WHERE i2.symbol = t.symbol ORDER BY ts DESC LIMIT 1
    ) i ON TRUE
    WHERE {' AND '.join(where)}
    ORDER BY i.squeeze_firing DESC, i.breakout_55d DESC
    LIMIT {int(limit)}
    """

    conn = await get_conn()
    try:
        rows = await conn.fetch(q, *params)
        return [dict(r) for r in rows]
    finally:
        await conn.close()
