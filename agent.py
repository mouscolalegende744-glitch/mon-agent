import os, json, datetime, urllib.request, urllib.error

MODEL = "gemini-flash-latest"
key = os.environ["GEMINI_API_KEY"]
skill = open("skill.md", encoding="utf-8").read()
task = open("task.txt", encoding="utf-8").read()

url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
body = {
    "systemInstruction": {"parts": [{"text": skill}]},
    "contents": [{"role": "user", "parts": [{"text": task}]}],
}
req = urllib.request.Request(
    url,
    data=json.dumps(body).encode(),
    headers={"Content-Type": "application/json", "x-goog-api-key": key},
)
try:
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.load(r)
except urllib.error.HTTPError as e:
    print("ERREUR GOOGLE", e.code, e.read().decode()[:800])
    raise SystemExit(1)

text = data["candidates"][0]["content"]["parts"][0]["text"]
os.makedirs("results", exist_ok=True)
name = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
open(f"results/{name}.md", "w", encoding="utf-8").write(text)
print(text)
