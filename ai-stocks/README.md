# AI Stocks Lite (FMP‑only)

A minimal screener + chart you can run with **only** your FMP API key.

## Quick start
1. Install Python 3.11+.
2. Create a folder and copy this `ai-stocks-lite` tree into it.
3. Copy `.env.example` to `.env` and set `FMP_API_KEY`.
4. Install deps & run the server:
   ```bash
   cd ai-stocks-lite/api
   python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ./run.sh   # Windows: bash run.sh
