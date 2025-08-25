import uvicorn
from fastapi import FastAPI
from .routes import health, prices, screener

app = FastAPI(title="AI Stocks API")
app.include_router(health.router)
app.include_router(prices.router)
app.include_router(screener.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
