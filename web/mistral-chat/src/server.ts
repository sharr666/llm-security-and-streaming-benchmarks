// Author: Mehrdad Poorhassan (Dr. Metal) - ORCID: 0009-0004-9269-3912
// SPDX-License-Identifier: Apache-2.0
import { createServer, type IncomingMessage, type ServerResponse } from "node:http";
import { existsSync, readFileSync } from "node:fs";
import { readFile } from "node:fs/promises";
import { extname, join, normalize, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";
import { Mistral } from "@mistralai/mistralai";

const MODEL = "mistral-small-latest";
const PORT = Number(process.env.PORT ?? 3000);
const MAX_BODY_BYTES = 64 * 1024;
const MAX_MESSAGES = 50;
const MAX_MESSAGE_CHARS = 8000;

const appDir = fileURLToPath(new URL("..", import.meta.url));
const publicDir = join(appDir, "public");

loadEnvFile(join(appDir, ".env"));

const apiKey = process.env.MISTRAL_API_KEY ?? "";
const client = new Mistral({ apiKey });

type ChatRole = "system" | "user" | "assistant";
interface ChatMessage {
  role: ChatRole;
  content: string;
}

function loadEnvFile(path: string): void {
  if (!existsSync(path)) return;
  for (const line of readFileSync(path, "utf8").split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eq = trimmed.indexOf("=");
    if (eq <= 0) continue;
    const key = trimmed.slice(0, eq).trim();
    const value = trimmed.slice(eq + 1).trim().replace(/^["']|["']$/g, "");
    if (process.env[key] === undefined) process.env[key] = value;
  }
}

function sendJson(res: ServerResponse, status: number, body: unknown): void {
  const data = JSON.stringify(body);
  res.writeHead(status, { "content-type": "application/json; charset=utf-8" });
  res.end(data);
}

function readBody(req: IncomingMessage): Promise<string> {
  return new Promise((resolveBody, reject) => {
    const chunks: Buffer[] = [];
    let size = 0;
    req.on("data", (chunk: Buffer) => {
      size += chunk.length;
      if (size > MAX_BODY_BYTES) {
        reject(new Error("body too large"));
        req.destroy();
        return;
      }
      chunks.push(chunk);
    });
    req.on("end", () => resolveBody(Buffer.concat(chunks).toString("utf8")));
    req.on("error", reject);
  });
}

function parseMessages(payload: unknown): ChatMessage[] {
  if (typeof payload !== "object" || payload === null || !Array.isArray((payload as { messages?: unknown }).messages)) {
    throw new Error('Expected a JSON body like { "messages": [{ "role": "user", "content": "..." }] }.');
  }
  const raw = (payload as { messages: unknown[] }).messages;
  if (raw.length === 0) throw new Error("messages must not be empty.");
  if (raw.length > MAX_MESSAGES) throw new Error(`Too many messages (max ${MAX_MESSAGES}).`);
  return raw.map((item, i) => {
    if (typeof item !== "object" || item === null) throw new Error(`messages[${i}] must be an object.`);
    const { role, content } = item as { role?: unknown; content?: unknown };
    if (role !== "system" && role !== "user" && role !== "assistant") {
      throw new Error(`messages[${i}].role must be "system", "user" or "assistant".`);
    }
    if (typeof content !== "string" || content.trim().length === 0) {
      throw new Error(`messages[${i}].content must be a non-empty string.`);
    }
    if (content.length > MAX_MESSAGE_CHARS) {
      throw new Error(`messages[${i}].content exceeds ${MAX_MESSAGE_CHARS} characters.`);
    }
    return { role, content };
  });
}

function extractText(content: unknown): string {
  if (typeof content === "string") return content;
  if (Array.isArray(content)) {
    return content
      .filter((part): part is { type: "text"; text: string } =>
        typeof part === "object" && part !== null && (part as { type?: unknown }).type === "text" && typeof (part as { text?: unknown }).text === "string")
      .map((part) => part.text)
      .join("");
  }
  return "";
}

async function handleChat(req: IncomingMessage, res: ServerResponse): Promise<void> {
  let raw: string;
  try {
    raw = await readBody(req);
  } catch {
    sendJson(res, 413, { error: "Request body too large." });
    return;
  }
  let payload: unknown;
  try {
    payload = JSON.parse(raw);
  } catch {
    sendJson(res, 400, { error: "Request body must be valid JSON." });
    return;
  }
  let messages: ChatMessage[];
  try {
    messages = parseMessages(payload);
  } catch (err) {
    sendJson(res, 400, { error: err instanceof Error ? err.message : String(err) });
    return;
  }
  if (!apiKey) {
    sendJson(res, 500, { error: "MISTRAL_API_KEY is not set on the server. Copy .env.example to .env and set your key." });
    return;
  }
  try {
    const completion = await client.chat.complete({ model: MODEL, messages });
    const reply = extractText(completion.choices?.[0]?.message?.content);
    sendJson(res, 200, { reply });
  } catch (err) {
    console.error("Mistral API error:", err instanceof Error ? err.message : err);
    sendJson(res, 502, { error: "The Mistral API request failed. Check the server logs." });
  }
}

const MIME_TYPES: Record<string, string> = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".ico": "image/x-icon",
  ".json": "application/json; charset=utf-8",
};

async function serveStatic(res: ServerResponse, pathname: string): Promise<void> {
  const rel = pathname === "/" ? "index.html" : pathname.slice(1);
  const filePath = resolve(join(publicDir, normalize(rel)));
  if (filePath !== publicDir && !filePath.startsWith(publicDir + sep)) {
    sendJson(res, 403, { error: "Forbidden" });
    return;
  }
  try {
    const data = await readFile(filePath);
    res.writeHead(200, { "content-type": MIME_TYPES[extname(filePath)] ?? "application/octet-stream" });
    res.end(data);
  } catch {
    sendJson(res, 404, { error: "Not found" });
  }
}

const server = createServer((req, res) => {
  const url = new URL(req.url ?? "/", "http://localhost");
  if (url.pathname === "/api/chat" && req.method === "POST") {
    void handleChat(req, res);
    return;
  }
  if (req.method === "GET" || req.method === "HEAD") {
    void serveStatic(res, url.pathname);
    return;
  }
  sendJson(res, 405, { error: "Method not allowed" });
});

server.listen(PORT, () => {
  console.log(`Chat app listening on http://localhost:${PORT} (model: ${MODEL})`);
  if (!apiKey) console.log("Warning: MISTRAL_API_KEY is not set; /api/chat will return an error until you configure it.");
});
