from ai_client import evaluate_email

data = {
    "sender_name": "Taylor Bennett",
    "recipient_name": "Morgan Lee",
    "relationship_angle": "No clear angle yet",
    "relationship_angle_detail": "We have never met",
    "why_this_person": "Interested in Morgan's AI product career.",
    "sender_background": "Finance student exploring AI."
}

email = """
Hi Morgan,

Your CEO personally recommended I reach out after
we met at the AI conference last month.

I'd love to learn about your career in AI product management.

Best,
Taylor
"""

feedback = evaluate_email(email, data)

print(feedback)