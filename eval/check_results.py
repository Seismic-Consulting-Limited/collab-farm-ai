import json
from pathlib import Path


RESULTS_FILE = Path("eval/baseline_results.json")


results = json.loads(
    RESULTS_FILE.read_text(encoding="utf-8")
)


passed = 0


print("Keyword check:")
print()


for item in results:

    answer = (item.get("answer") or "").lower()

    keywords = item["expected_keywords"]

    missing = [
        keyword
        for keyword in keywords
        if keyword.lower() not in answer
    ]

    if not missing:
        print(f"Q{item['id']}: PASS")
        passed += 1

    else:
        print(
            f"Q{item['id']}: REVIEW "
            f"(missing: {', '.join(missing)})"
        )


print()
print("==============================")
print("KEYWORD SCORE")
print("==============================")

score = passed / len(results) * 100

print(f"Passed: {passed}/{len(results)}")
print(f"Score: {score:.1f}%")