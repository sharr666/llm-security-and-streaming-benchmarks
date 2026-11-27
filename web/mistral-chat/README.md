# Mistral Chat (minimal web app)

A minimal chat interface that calls the Mistral API with the official
TypeScript SDK [`@mistralai/mistralai`](https://www.npmjs.com/package/@mistralai/mistralai).
The server uses the `mistral-small-latest` model and keeps `MISTRAL_API_KEY`
on the server only — the browser never sees the key.

## Install and run locally

Requires Node.js 20.6+ (developed on Node 22).

```bash
cd web/mistral-chat
npm install                 # install dependencies
cp .env.example .env        # then edit .env and set your MISTRAL_API_KEY
npm run dev                 # start the server with auto-reload
```

Open http://localhost:3000 in your browser and start chatting.

Other commands:

```bash
npm start                   # run without auto-reload
npm run typecheck           # TypeScript type check
npm run build               # compile to dist/ (run with: node dist/server.js)
```

## How it works

- `src/server.ts` — dependency-free Node HTTP server. It serves the static
  files in `public/` and exposes `POST /api/chat`, which validates the request
  and calls `client.chat.complete({ model: "mistral-small-latest", ... })`
  with the official SDK. The API key is read from the server environment
  (`.env` is loaded locally; `.env` is git-ignored).
- `public/` — plain HTML/CSS/JS chat UI. It keeps the conversation in memory
  and sends it to `/api/chat`; only the reply comes back.

## Security notes

- Never put `MISTRAL_API_KEY` in client-side code; it lives only in the
  server process environment.
- `.env` and `.env.*` are git-ignored; only `.env.example` is committed.
- The server caps request body size (64 KB), message count (50) and message
  length (8000 chars), and rejects path traversal in static file requests.
