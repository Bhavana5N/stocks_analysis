import os, asyncpg
DB_DSN = os.getenv("DB_DSN", "postgres://%s:%s@db:5432/%s" % (
  os.getenv("POSTGRES_USER", "postgres"),
  os.getenv("POSTGRES_PASSWORD", "postgres"),
  os.getenv("POSTGRES_DB", "stocks")))
async def get_conn():
    return await asyncpg.connect(dsn=DB_DSN)
