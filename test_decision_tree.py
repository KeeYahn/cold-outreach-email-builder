def should_revise(evaluation):
    score = evaluation["overall_score"]
    issue = evaluation["issue_type"]
    recommendation = evaluation["revision_recommended"]
    required_keys = {
            "overall_score",
            "issue_type",
            "revision_recommended",
        }
    if not required_keys.issubset(evaluation.keys()):
        raise ValueError("Evaluation is missing required fields.")
    score = evaluation["overall_score"]
    ALLOWED_ISSUES = {
        "none",
        "grammar",
        "typo",
        "sender_focus",
        "personalization",
        "clarity",
        "structure",
        "misrepresentation"
    }

    issue = evaluation["issue_type"]
    recommendation = evaluation["revision_recommended"]
    # weakness = evaluation["weaknesses"] # Not used in this test case
    # reasons = evaluation["reason"] # Not used in this test case

    if issue == "misrepresentation":
        return True
    elif score < 8:
        return True
    elif recommendation == True and issue in ALLOWED_ISSUES:
        return True
    else:
        return False

# Test 1: Strong email, no issues
test_1 = {
    "overall_score": 9,
    "issue_type": "grammar",
    "revision_recommended": False
}

# Test 2: Weak email
test_2 = {
    "overall_score": 9,
    "issue_type": "misrepresentation",
    "revision_recommended": False
}

assert should_revise(test_1) == False
assert should_revise(test_2) == True

print("All tests passed!")



"""print("Decision Tree Terminal Tester")
print ("Type 'quit' at any time to exit the loop.\n")
while True:
    issue_input = input('1. Enter Issue Type (e.g. grammar, typo, sender_focus, personalization, misrepresentation, clarity, structure):').strip().lower()
    if issue_input == 'quit':
        break
    score_input = input("2. Enter overall score (1-10): ").strip()
    if score_input.lower() == 'quit':
        break
    try:
        score_val = int(score_input)
    except ValueError:
        print("Invalid Input. Score must be an integer from 1-10. Restarting loop.")
        continue
    rec_input = input("3. Revision recommended by LLM? (yes/no): ")
    if rec_input == 'quit':
        break
    rec_bool = rec_input in ['yes', 'y', 'true']
    mock_evaluation = {
        "overall_score": score_val,
        "issue_type": issue_input,
        "revision_recommendation": rec_bool,
        "weaknesses": [],
        "reason": []
        }
    try:
        verdict = should_revise(mock_evaluation)
        print(f"Test inputs: Issue = {issue_input}, Score = {score_val}, Recommendation = {rec_bool}")
        if verdict:
            print("Should revise")
        else:
            print("Don't revise")
    except Exception as e:
        print(f"Error during evaluation.")"""