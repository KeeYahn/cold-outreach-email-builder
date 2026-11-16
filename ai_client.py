import requests
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompt_template import evaluation_prompt, revision_prompt
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


# Step 1: Generate Email from the first prompt and user inputs -> data  (SDK API Call)
def generate_email(prompt):
    """Send the generated prompt to the AI model and return the response text."""

    if not api_key:
        raise ValueError(
            "Missing OPENAI_API_KEY. Add it to a .env file in your project folder."
        )
    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
    )

    return response.output_text


# Step 2: Evaluate the rough draft based on criteria dictated in the prompt (Raw API Call)
# Revised the term "data" in API Call to "payload" to avoid data library rewriting.
def evaluate_email(email, data):
    """Evaluate the rough draft for emails and provide structured, digestible feedback."""

    if not api_key:
        raise ValueError(
            "Missing OPENAI_API_KEY. Add it to an .env file in your project folder."
        )

    url = "https://api.openai.com/v1/responses"
    headers = {
        "Authorization":f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = evaluation_prompt(email, data)
    payload = {
        "model": "gpt-5-mini",
        "input": prompt,
    }

    #Formats the body of the API call, and parses the HTTP response into Python data for us.
    response = requests.post(url, headers=headers, json=payload, timeout=60)

    #This if statement deals with one of the more prominent status codes (200).
    if response.status_code != 200:
        print(response.status_code, response.text)
        raise ValueError("Evaluation failed")

    response_data = response.json()

    # Extract, parse, and validate the model-generated evaluation.
    # STEP 1: Extract the model's response text from the API response.
    # response_data is already a Python dictionary created by response.json(). Look above like 10 lines for us parsing the whole HTTP response.
    # The model-generated evaluation inside "text" is still a JSON string.
    try:
        for item in response_data["output"]:
            if item["type"] == "message":
                raw_text = item["content"][0]["text"]

    #This section down below deals with conversion from JSON string to python data.
    # STEP 2: Parse the JSON string into a Python object.
    # Parsing alone does not guarantee the result is a dictionary. We will have safeguards down below for that.
                try:
                    evaluation = json.loads(raw_text)
                    if not isinstance(evaluation, (dict)):
                        raise ValueError("Evaluation must be a dictionary, not a list, string, None, or Boolean!")

    #This section validates required keys for the python dictionary.
    # STEP 3: Validate the required dictionary keys.
    # main.py and the revision workflow depend on these fields, to edit this, also edit prompt_template.py.
                    required_keys = {
                            "overall_score",
                            "issue_type",
                            "revision_recommended",
                            "weaknesses",
                            "reason"
                        }
                    if not required_keys.issubset(evaluation.keys()):
                        raise ValueError("Evaluation is missing required fields.")

    #This section provides a guard rail by saying "here are the issues that are within our consideration in the library," raise errors for those not listed here and have them formatted as strings.
    # STEP 4: Extract values and define allowed issue categories.
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
                    weakness = evaluation["weaknesses"]
                    reasons = evaluation["reason"]
    #All of the formatting things and evaluation errors, including the overall score being a numeric value, recommendations being boolean (0 or 1/True or False), issue type being a string from the dic above.
    # STEP 5: Validate types and allowed values.
    # Reject unexpected data before main.py uses the evaluation.
                    if not isinstance(issue, (str)):
                        raise ValueError("Issue Type must be a string.")
                    if issue not in ALLOWED_ISSUES:
                        raise ValueError("Unrecognized issue type.")
                    if not isinstance(recommendation, (bool)):
                        raise ValueError("Revision Recommendation must be a Boolean.")
                    if not isinstance(score, (int, float)) or isinstance(score, bool):
                        raise ValueError("Evaluation score must be numeric and not boolean.")
                    if score < 1 or score > 10:
                        raise ValueError("Score is outside the valid range. Keep it between 1-10.")
                    if not isinstance(weakness, (list)) or not all(isinstance(item, str) for item in weakness):
                        raise ValueError("Weaknesses must be a list of strings.")
                    if not isinstance(reasons, (str)):
                        raise ValueError("Weakness Reason must be a string.")

    #Closes out the "Try" funtion, handles incorrect JSOn syntax.
    # STEP 6: Handle malformed JSON syntax.
    # This catches parsing failures, not every validation error.
    # The original error is preserved for debugging.
                except json.JSONDecodeError as error:
                        raise ValueError("The AI returned invalid JSON for the Evaluation.") from error
    # STEP 7: Return the parsed, partially validated evaluation.
                return evaluation

    #Only reached if no valid message was returned (prevents empty spaces or "None").
        raise ValueError("No evaluation message found in API response.")

    # Existing fallback: API response fields were missing or inaccessible.
    except(KeyError, IndexError) as error:
        print(response.json())
        raise ValueError("Failed to parse AI evaluation.") from error


# Step 3: Revise rough draft based on evaluation/feedback in step 2.  (raw API Call -> shown through requests.post())
def revise_email(email, feedback, data):
    """Revise the rough draft based on the evaluation."""

    if not api_key:
        raise ValueError(
        "Missing OPENAI_API_KEY. Add it to an .env file in your project folder."
        )

    url = "https://api.openai.com/v1/responses"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = revision_prompt(email, feedback, data)
    payload = {
            "model": "gpt-5-mini",
            "input": prompt,
        }
    response = requests.post(url, headers=headers, json=payload, timeout=60)

    if response.status_code !=200:
        print(response.status_code, response.text)
        raise ValueError(f"Revision API failed with status {response.status_code}")

    response_data = response.json()

    try:
        for item in response_data["output"]:
            if item["type"] == "message":
                return item["content"][0]["text"]
        raise ValueError("No revision message found in API response.")

    except (KeyError, IndexError) as error:
        raise ValueError("Failed to parse AI revision.") from error