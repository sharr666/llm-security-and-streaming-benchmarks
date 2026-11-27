// Author: Mehrdad Poorhassan (Dr. Metal) - ORCID: 0009-0004-9269-3912
// SPDX-License-Identifier: Apache-2.0
const messagesEl = document.getElementById("messages");
const form = document.getElementById("composer");
const input = document.getElementById("prompt");
const sendBtn = document.getElementById("send");

const history = [];

function addBubble(role, text) {
  const bubble = document.createElement("div");
  bubble.className = `message ${role}`;
  const label = document.createElement("span");
  label.className = "role";
  label.textContent = role === "user" ? "You" : "Mistral";
  const body = document.createElement("p");
  body.textContent = text;
  bubble.append(label, body);
  messagesEl.appendChild(bubble);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return body;
}

async function send() {
  const text = input.value.trim();
  if (!text || sendBtn.disabled) return;
  input.value = "";
  history.push({ role: "user", content: text });
  addBubble("user", text);
  sendBtn.disabled = true;
  const pending = addBubble("assistant", "…");
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ messages: history }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || `Request failed (${res.status})`);
    history.push({ role: "assistant", content: data.reply });
    pending.textContent = data.reply;
  } catch (err) {
    pending.textContent = `Error: ${err.message}`;
    pending.classList.add("error");
  } finally {
    sendBtn.disabled = false;
    input.focus();
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  void send();
});

input.focus();
