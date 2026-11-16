import json

raw_text = "Evaluation failed"

try:
    evaluation = json.loads(raw_text)
    print("Successfully parsed:", evaluation)

except json.JSONDecodeError:
    print("Invalid JSON detected. Parsing stopped safely.")

print("Test completed.")