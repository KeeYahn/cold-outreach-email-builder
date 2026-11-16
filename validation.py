import re

ASK_PRESETS = {
    "15-20 minute conversation": (
        "Would you be open to a 15-20 minute conversation sometime in the next few weeks?"
    ),
    "quick phone call": (
        "Would you be open to a quick phone call sometime in the next few weeks?"
    ),
    "virtual coffee chat": (
        "Would you be open to a virtual chat sometime in the next few weeks?"
    ),
    "in-person coffee chat": (
        "Would you be open to an in-person chat sometime in the next few weeks? I would like to treat you to coffee, tea, or a drink."
    ),
    "informational interview": (
        "Would you be open to a brief informational interview about your career path?"
    ),
    "email advice only": (
        "If you have time, I'd really appreciate any brief advice over email. No meeting needed."
    ),
    "open to staying in touch": (
        "I'd love to stay in touch and would welcome any advice you might be willing to share when convenient."
    ),
}


def normalize_ask(ask_input):
    """
    Turn flexible ask inputs into a clear call-to-action for the prompt.

    Examples:
    - "Quick 10-minute call" -> full low-pressure ask sentence
    - "coffee chat next week" -> wrapped into a polite ask
    - "Would you be open to chatting?" -> passed through as-is
    """
    text = (ask_input or "").strip()
    if not text:
        return ASK_PRESETS["15-20 minute conversation"]

    lower = text.lower()

    if text.endswith("?") or (
        re.search(
            r"\b(would|could|open to|appreciate|wondering|ask|invite|love to|hope)\b",
            lower,
        )
        and len(text.split()) >= 6
    ):
        return text if text.endswith((".", "?")) else f"{text}."

    if lower in ASK_PRESETS:
        return ASK_PRESETS[lower]

    if lower == "other":
        return ASK_PRESETS["15-20 minute conversation"]

    return f"Would you be open to {text}?"

TONE_PRESETS = {
    "formal": (
        "Write in a polished, professional tone. Use complete sentences and "
        "avoid slang or overly casual phrasing."
    ),
    "casual-professional": (
        "Write in a warm, approachable tone that still feels respectful and "
        "professional — not stiff, but not overly casual."
    ),
    "warm": (
        "Write in a warm, personable tone. Sound genuine and human without "
        "being overly familiar."
    ),
    "curious": (
        "Write in a curious, interested tone. Show thoughtful engagement "
        "without sounding like an interview."
    ),
    "confident": (
        "Write in a confident, clear tone. Be direct and purposeful without "
        "sounding arrogant or pushy."
    ),
    "respectful": (
        "Write in a respectful, considerate tone. Acknowledge the recipient's "
        "time and experience without being deferential or needy."
    ),
    "conversational / friendly": (
        "Write in a conversational, friendly tone. Keep it natural and easy "
        "to read, like a thoughtful note to someone you respect."
    ),
}

def normalize_tone(tone_input):
    """
    Turn flexible tone inputs into a clear instruction for the prompt.

    Examples:
    - "Warm" -> expanded preset instruction
    - "mentor-like but not stiff" -> wrapped custom instruction
    - "Write in a warm, curious voice." -> passed through as-is
    """
    text = (tone_input or "").strip()
    if not text:
        return TONE_PRESETS["casual-professional"]

    lower = text.lower()

    if re.search(
        r"\b(write|sound|voice|tone|style|manner|approach|avoid)\b",
        lower,
    ) and len(text.split()) >= 4:
        return text if text.endswith(".") else f"{text}."

    if lower in TONE_PRESETS:
        return TONE_PRESETS[lower]

    return f"Write in a {text} tone."


def normalize_length(length_input):
    """
    Turn flexible length inputs into a clear instruction for the prompt.

    Examples:
    - "75" -> approximately 75 words
    - "75 words" -> approximately 75 words
    - "75-125" or "75-125 words" -> approximately 75-125 words
    - "Write the email body in exactly 75 words." -> passed through as-is
    """
    text = (length_input or "").strip()
    if not text:
        return "Write the email body in approximately 75-125 words."

    lower = text.lower()

    if re.search(
        r"\b(write|keep|limit|around|about|approximately|exactly|no more than|at most|at least)\b",
        lower,
    ) and len(text.split()) >= 4:
        return text if text.endswith(".") else f"{text}."

    range_match = re.search(r"(\d+)\s*(?:-|to)\s*(\d+)", lower)
    if range_match:
        low, high = range_match.groups()
        return f"Write the email body in approximately {low}-{high} words."

    about_match = re.search(
        r"(?:about|around|approximately|~)\s*(\d+)\s*(?:words?)?", lower
    )
    if about_match:
        count = about_match.group(1)
        return f"Write the email body in approximately {count} words."

    if re.fullmatch(r"exactly\s+(\d+)\s*(?:words?)?\.?", lower):
        count = re.fullmatch(r"exactly\s+(\d+)\s*(?:words?)?\.?", lower).group(1)
        return f"Write the email body in exactly {count} words."

    single_match = re.search(r"(\d+)\s*(?:words?)?", lower)
    if single_match:
        count = single_match.group(1)
        if "exact" in lower:
            return f"Write the email body in exactly {count} words."
        return f"Write the email body in approximately {count} words."

    return text if text.endswith(".") else f"Length guidance: {text}."


def is_too_short(text, minimum_words):
    """Check whether a text response has fewer words than a minimum."""
    return len(text.split()) < minimum_words

def contains_generic_language(text):
    """Check for vague phrases that often lead to generic outreach."""
    generic_phrases = [
        "learn more",
        "your experience",
        "your background",
        "connect",
        "network",
        "interesting career",
        "pick your brain",
        "hope this email finds you well",
        "reaching out",
        "following up",
        "touch base",
        "hop on a call",
        "reach out",
        "checking in",
        "per my last email",
        "per our conversation",
        "as discussed",
        "as previously stated",
        "nice to e-meet you",
        "I know you are busy",
        "I know you're busy",
        "came across your profile",
        "your career path is inspiring",
        "your insights would be invaluable",
        "thank you for your consideration",
        "your impressive background",
        "looking forward to your reply"
    ]

    lower_text = text.lower()
    for phrase in generic_phrases:
        if phrase in lower_text:
            return True
    return False


def format_optional_for_prompt(value, absent_message):
    """Return user text when provided, otherwise a clear do-not-invent instruction."""
    text = (value or "").strip()
    if text:
        return text
    return absent_message


def validate_inputs(data):
    """
    Review the user's inputs and return a list of warnings.
    These warnings do not stop the program.
    They help the user understand where the email may be weak.
    """

    warnings = []

    if data["relationship_angle"] == "No clear angle yet":
        warnings.append(
            "No clear relationship angle was selected. The email may be more generic unless you add a stronger reason for reaching out."
        )
    if is_too_short(data["why_this_person"], 8):
        warnings.append(
            "'Why this person stood out' is short. Add a specific detail about their role, company, career path, or experience."
        )
    if is_too_short(data["what_the_sender_wants_to_learn"], 8):
        warnings.append(
            "'What you want to learn' is short. Make the learning goal more specific so the ask feels intentional."
        )
    if contains_generic_language(data["why_this_person"]):
        warnings.append(
            "'Why this person stood out' may be too generic. Try making a specific career move, company, role, industry, or shared context."
        )
    if contains_generic_language(data["what_the_sender_wants_to_learn"]):
        warnings.append(
            "'What you want to learn' may be too broad. Try specifying the exact topics you want advice on."
        )
    if data["relationship_angle"] != "No clear angle yet" and not data["relationship_angle_detail"].strip():
        warnings.append(
            "A relationship angle category was selected, but no detail was provided. The tool can use the category, but the email may feel stronger with one specific detail."
        )

    return warnings

def apply_defaults(data):
    """Add default values if certain optional fields are missing."""

    if not data.get("ask"):
        data["ask"] = "15-20 minute conversation"
    data["ask_instruction"] = normalize_ask(data["ask"])
    if not data.get("tone"):
        data["tone"] = "Casual-Professional"
    data["tone_instruction"] = normalize_tone(data["tone"])
    if not data.get("length"):
        data["length"] = "75-125 words"
    data["length_instruction"] = normalize_length(data["length"])

    data["sender_experience_for_prompt"] = format_optional_for_prompt(
        data.get("sender_experience"),
        "None provided — do not invent experience beyond the background.",
    )
    data["relationship_detail_for_prompt"] = format_optional_for_prompt(
        data.get("relationship_angle_detail"),
        "None provided — use the relationship angle only; do not invent specific shared history.",
    )
    return data
