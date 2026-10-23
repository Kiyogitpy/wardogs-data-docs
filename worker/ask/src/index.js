// "Ask the docs" answer endpoint. The browser does the retrieval (it already holds the site's
// search index) and posts the question with the best-matching sections; this Worker only asks
// the model to answer from those sections and returns the text. It keeps no state and no keys:
// the model runs through the Workers AI binding, whose free daily allowance caps total use.

const MODEL = "@cf/meta/llama-3.1-8b-instruct";
const MAX_QUESTION = 300;
const MAX_SOURCES = 6;
const MAX_SOURCE_CHARS = 1800;

const SYSTEM = [
  "You answer questions about the game Wardogs using only the numbered excerpts from its data reference.",
  "Cite the excerpts you use as [1], [2] after the statement they support.",
  "Quote numbers exactly as written. Never guess or add facts that are not in the excerpts.",
  "If the excerpts do not answer the question, say so in one sentence.",
  "Keep the answer under 150 words.",
].join(" ");

function cors(origin, env) {
  const allowed = (env.ALLOWED_ORIGINS || "").split(",").map((s) => s.trim()).filter(Boolean);
  const ok = allowed.includes(origin);
  return {
    ok,
    headers: {
      "Access-Control-Allow-Origin": ok ? origin : allowed[0] || "",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Vary": "Origin",
    },
  };
}

function reply(body, status, headers) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...headers, "Content-Type": "application/json" },
  });
}

export function parseRequest(body) {
  const question = typeof body?.question === "string" ? body.question.trim() : "";
  if (!question || question.length > MAX_QUESTION) return null;
  if (!Array.isArray(body.sources) || !body.sources.length || body.sources.length > MAX_SOURCES) return null;
  const sources = [];
  for (const s of body.sources) {
    if (typeof s?.title !== "string" || typeof s?.text !== "string") return null;
    sources.push({ title: s.title.slice(0, 200), text: s.text.slice(0, MAX_SOURCE_CHARS) });
  }
  return { question, sources };
}

export function buildMessages({ question, sources }) {
  const excerpts = sources.map((s, i) => `[${i + 1}] ${s.title}\n${s.text}`).join("\n\n");
  return [
    { role: "system", content: SYSTEM },
    { role: "user", content: `Excerpts:\n\n${excerpts}\n\nQuestion: ${question}` },
  ];
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const { ok, headers } = cors(origin, env);
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers });
    if (request.method !== "POST" || !ok) return reply({ error: "not allowed" }, 403, headers);

    if (env.LIMITER) {
      const key = request.headers.get("CF-Connecting-IP") || "unknown";
      const { success } = await env.LIMITER.limit({ key });
      if (!success) return reply({ error: "rate limited" }, 429, headers);
    }

    let parsed;
    try {
      parsed = parseRequest(await request.json());
    } catch {
      parsed = null;
    }
    if (!parsed) return reply({ error: "bad request" }, 400, headers);

    try {
      const out = await env.AI.run(MODEL, { messages: buildMessages(parsed), max_tokens: 400 });
      return reply({ answer: String(out.response || "").trim() }, 200, headers);
    } catch {
      return reply({ error: "model unavailable" }, 502, headers);
    }
  },
};
