import json
import time
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.chatbot.chatbot import chat

QUESTIONS_FILE = ROOT / "eval" / "questions.jsonl"
RESULTS_FILE = ROOT / "eval" / "baseline_results.json"

results = []

questions = [
    json.loads(line)
    for line in QUESTIONS_FILE.read_text(encoding="utf-8-sig").splitlines()
    if line.strip()
]

print(f"Running {len(questions)} baseline questions...\n")

for i, item in enumerate(questions, start=1):
    session_id = f"baseline-{item['id']}-{int(time.time())}"

    print(f"[{i}/{len(questions)}] {item['question']}")

    start = time.perf_counter()

    try:
        response = chat(
            item["question"],
            session_id
        )

        answer = response.get("answer", "")

        elapsed = time.perf_counter() - start

        results.append({
            "id": item["id"],
            "category": item["category"],
            "question": item["question"],
            "expected_keywords": item["expected"],
            "answer": answer,
            "latency_seconds": round(elapsed, 3),
            "error": None
        })

        print(f"    OK ({elapsed:.2f}s)")

    except Exception as e:
        elapsed = time.perf_counter() - start

        results.append({
            "id": item["id"],
            "category": item["category"],
            "question": item["question"],
            "expected_keywords": item["expected"],
            "answer": None,
            "latency_seconds": round(elapsed, 3),
            "error": str(e)
        })

        print(f"    ERROR: {e}")

RESULTS_FILE.write_text(
    json.dumps(results, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("\n================================")
print("BASELINE COMPLETE")
print("================================")
print(f"Questions: {len(results)}")
print(f"Results: {RESULTS_FILE}")
