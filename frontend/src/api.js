export async function chatWithBot(question) {
  const res = await fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({question})
  });
  return await res.json();
}

export async function summarizeText(text) {
  const res = await fetch("http://localhost:8000/summarize", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({text})
  });
  return await res.json();
}
