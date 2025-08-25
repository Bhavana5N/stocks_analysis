from ..celery import app
import asyncpg, os, httpx

DB = os.getenv("DB_DSN", "postgres://postgres:postgres@db:5432/stocks")
TG = os.getenv("TELEGRAM_BOT_TOKEN"); CHAT = os.getenv("TELEGRAM_CHAT_ID")

@app.task
def scan_and_alert():
    import asyncio
    asyncio.run(_run())

async def _run():
    if not TG or not CHAT: return
    conn = await asyncpg.connect(dsn=DB)
    try:
        rows = await conn.fetch("""
          WITH last AS (
            SELECT DISTINCT ON (symbol) symbol, ts, squeeze_firing, near_breakout
            FROM indicators ORDER BY symbol, ts DESC)
          SELECT symbol FROM last WHERE squeeze_firing AND near_breakout
        """)
        if not rows: return
        async with httpx.AsyncClient(timeout=15) as client:
            for r in rows:
                await client.post(f"https://api.telegram.org/bot{TG}/sendMessage",
                  json={"chat_id": CHAT, "text": f"🚀 {r['symbol']} squeeze firing near breakout"})
    finally:
        await conn.close()
