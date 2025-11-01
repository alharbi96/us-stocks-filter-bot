# Deploy as Web Service on Render

This variant exposes a minimal Flask web endpoint and runs the original worker loop in a background thread.

## Quick start
1. Connect the repo to Render.
2. Render auto-detects `render.yaml`. It will create a **Web Service** with:
   - Build: `pip install -r requirements.txt`
   - Start: `python -m app.server`
3. Add env vars:
   - `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` (required for Telegram messages)
   - `MARKETDATA_API_KEY`, `MARKETDATA_BASE_URL` (if using real market data)
   - For testing: set `MARKETDATA_MOCK=true`
4. Health endpoint: `GET /` returns `{"status":"ok"}`
   Optional status: `GET /status`

## Notes
- The server binds to `0.0.0.0` and reads port from `$PORT` (Render provides it).
- The worker loop from `app.main.run()` continues to function as before.
- If you prefer **Background Worker** instead, change `type` back to `worker` and `startCommand: python -m app.main`.
