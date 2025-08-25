from ..celery import app
import asyncpg, os, pandas as pd, pandas_ta as ta

DB = os.getenv("DB_DSN", "postgres://postgres:postgres@db:5432/stocks")

@app.task
def compute_indicators(symbol: str):
    import asyncio
    asyncio.run(_run(symbol))

async def _run(symbol: str):
    conn = await asyncpg.connect(dsn=DB)
    try:
        rows = await conn.fetch("""
            SELECT ts,o,h,l,c,v FROM prices WHERE symbol=$1 AND interval='1d' ORDER BY ts
        """, symbol)
        if not rows: return
        df = pd.DataFrame(rows, columns=["ts","o","h","l","c","v"]).set_index("ts")
        sp = ta.squeeze_pro(high=df["h"], low=df["l"], close=df["c"])
        squeeze_on = sp["SQZ_PRO_ON"].astype(bool)
        mom = sp["SQZ_PRO_MOM"]
        firing = (mom > 0) & (mom.shift(1) <= 0)
        hh55 = df["c"].rolling(55).max()
        breakout = (df["c"] >= hh55).fillna(False)
        near = (((hh55 - df["c"]) / hh55).between(0, 0.03)) & squeeze_on
        last_ts = df.index[-1].to_pydatetime()
        await conn.execute(
            """
            INSERT INTO indicators(symbol, ts, squeeze_on, squeeze_firing, momentum, breakout_55d, near_breakout)
            VALUES($1,$2,$3,$4,$5,$6,$7)
            ON CONFLICT (symbol, ts) DO UPDATE SET
              squeeze_on=EXCLUDED.squeeze_on,
              squeeze_firing=EXCLUDED.squeeze_firing,
              momentum=EXCLUDED.momentum,
              breakout_55d=EXCLUDED.breakout_55d,
              near_breakout=EXCLUDED.near_breakout
            """,
            symbol, last_ts, bool(squeeze_on.iloc[-1]), bool(firing.iloc[-1]), float(mom.iloc[-1]), bool(breakout.iloc[-1]), bool(near.iloc[-1])
        )
    finally:
        await conn.close()
