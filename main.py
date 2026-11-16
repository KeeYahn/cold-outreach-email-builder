
from prompt_template import build_outreach_prompt
from validation import validate_inputs, apply_defaults
from ai_client import generate_email, evaluate_email, revise_email


def ask_required(question):
    """Ask a required question until the user provides a non-empty answer."""
    while True:
        answer = input(question).strip()
        if answer:
            return answer
        print("This field is required. Please enter a response.")

def ask_optional(question):
    """Ask an optional question. Empty responses are allowed."""
    return input(question).strip()

def ask_with_default(question, default):
    """Ask a question, but use a default answer if the user leaves it blank."""
    answer = input(f"{question} [{default}]: ").strip()
    return answer if answer else default

def choose_relationship_angle():
    """Let the user choose a relationship angle from a menu."""
    options = [
        "Same school / alumni",
        "Same hometown / region",
        "Similar career path / industry",
        "Shared career interest",
        "Same role / function / interest",
        "Mutual connection",
        "Event / Webinar / Panel connection",
        "Shared personal interest",
        "Mission / value alignment",
        "No clear angle yet"
    ]

    print("\nChoose the relationship angle:")
    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")

    while True:
        choice = input("Enter a number from 1-10: ").strip()

        if choice.isdigit():
            choice_number = int(choice)
            if 1 <= choice_number <= len(options):
                return options[choice_number - 1]
        print("Invalid choice. Please enter a number from 1-10.")

def choose_ask():
    """Let the user choose an ask from a menu and/or write their own."""
    options = [
        "15-20 minute conversation",
        "Quick phone call",
        "Virtual coffee chat",
        "In-person coffee chat",
        "Informational interview",
        "Email advice only",
        "Open to staying in touch",
        "Other",
    ]

    print("\nChoose your ask:")
    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")

    while True:
        choice = input("Enter a number from 1-8: ").strip()

        if choice.isdigit():
            choice_number = int(choice)
            if 1 <= choice_number <= len(options):
                return options[choice_number - 1]
        print("Invalid choice. Please enter a number from 1-8.")


def choose_tone_style():
    """Let the user choose a tone style from a menu and/or add their own writing style."""
    options = [
        "Formal",
        "Casual-Professional",
        "Warm",
        "Curious",
        "Confident",
        "Respectful",
        "Conversational / Friendly",
        "Other",
    ]

    print("\nChoose the tone style:")
    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")

    while True:
        choice = input("Enter a number from 1-8: ").strip()

        if choice.isdigit():
            choice_number = int(choice)
            if 1 <= choice_number <= len(options):
                return options[choice_number - 1]
        print("Invalid choice. Please enter a number from 1-8.")

def get_word_count():
    while True:
        length_input = input("Desired email length in words [default: 100]: "
        ).strip()
        """Use the default if the user presses Enter"""
        if length_input == "":
            return 100
        try:
            word_count = int(length_input)
            if 20 <= word_count <= 300:
                return word_count
            elif word_count < 20:
                print("Too short, please pick a number between 20-300.")
            elif word_count > 300:
                print("Too long, please pick a number between 20-300.")
        except ValueError:
            print("Please enter a whole number, such as 75 or 120.")

def create_length_range(target):
    while True:
        range_input = input(
            "Desired range from word count [Default: 10. Ex: 50 words, Range: 45-55.] "
            "or type 'custom' to enter a custom range: "
        ).strip().lower()

        if range_input == "":
            default_tolerance = 10
            minimum = max(20, target - default_tolerance)
            maximum = min(300, target + default_tolerance)
            return minimum, maximum

        if range_input == "custom":
            while True:
                try:
                    custom_minimum = int(input("Minimum word count: ").strip())
                    custom_maximum = int(input("Maximum word count: ").strip())
                except ValueError:
                    print("Please enter whole numbers for both minimum and maximum.")
                    continue

                if custom_minimum < 20 or custom_maximum > 300:
                    print("Please use a range between 20 and 300 words.")
                    continue
                if custom_minimum >= custom_maximum:
                    print("Minimum must be less than maximum.")
                    continue

                return custom_minimum, custom_maximum

        try:
            tolerance = int(range_input)
            if 1 <= tolerance <= 50:
                minimum = max(20, target - tolerance)
                maximum = min(300, target + tolerance)
                return minimum, maximum
            print("Please enter a number between 1 and 50.")
        except ValueError:
            print("Please enter a whole number, 'custom', or press Enter for default.")


def collect_user_inputs():
    """Collect sender and recipient information from the terminal."""

    print("\n--- Sender Profile ---")
    sender_name = ask_required("Your name: ")
    sender_background = ask_required("Your one-sentence background: ")
    sender_experience = ask_optional("Relevant work history / experience: ")
    sender_goals = ask_required("Current career interest or goal: ")

    print("\n--- Recipient Context ---")
    recipient_name = ask_required("Recipient name: ")
    recipient_role_background = ask_required("Recipient role and company: ")
    why_this_person = ask_required("Why did this person stand out? ")
    what_the_sender_wants_to_learn = ask_required("What do you want to learn from them? ")

    relationship_angle = choose_relationship_angle()
    relationship_angle_detail = ask_optional(
        "Add a short detail about your relationship with this recipient, if you have one: "
    )

    ask_choice = choose_ask()
    if ask_choice == "Other":
        ask = ask_required("Describe the ask you want in the email: ")
    else:
        ask = ask_choice

    tone_choice = choose_tone_style()
    if tone_choice == "Other":
        tone = ask_required("Describe the tone you want for the email: ")
    else:
        tone = tone_choice

    target_word_count = get_word_count()
    print(f"Target length: approximately {target_word_count} words.")

    minimum, maximum = create_length_range(target_word_count)
    print(f"Write this email in approximately {minimum}-{maximum} words.")
    length = f"{minimum}-{maximum} words"

    return {
        "sender_name": sender_name,
        "sender_background": sender_background,
        "sender_experience": sender_experience,
        "sender_goals": sender_goals,
        "recipient_name": recipient_name,
        "recipient_role_background": recipient_role_background,
        "why_this_person": why_this_person,
        "what_the_sender_wants_to_learn": what_the_sender_wants_to_learn,
        "relationship_angle": relationship_angle,
        "relationship_angle_detail": relationship_angle_detail,
        "ask": ask,
        "tone": tone,
        "length": length
    }


# New decision function
def should_revise(evaluation):
    score = evaluation["overall_score"]
    issue = evaluation["issue_type"]
    recommendation = evaluation["revision_recommended"]

    if issue == "misrepresentation":
        return True
    elif score < 8: #Change this score if you want this value to increase or decrease
        return True
    elif recommendation and issue != "none":
        return True
    else:
        return False


# Tasks actually ran through terminal through execution of "python main.py". What the user actually interacts with and sees.
# Steps below are interactions between main.py, the user, and ai_client.py, in other words, API calls using prompts outlined in prompt_template.py
def main():
    data = collect_user_inputs()

    data = apply_defaults(data)
    warnings = validate_inputs(data)
    data["context_warnings"] = warnings

    if warnings:
        print("\n" + "=" *60)
        print("CONTEXT/USER INPUT WARNINGS")
        print("=" * 60)

        for warning in warnings:
            print(f"- {warning}")

    # Step 1: Build Prompts for Rough Draft
    prompt = build_outreach_prompt(data)

    # Step 2: Generate email (1st API Call)
    email = generate_email(prompt)
    print("\n" + "=" * 60)
    print("GENERATED EMAIL")
    print("=" * 60)
    print(email)

    # Step 3: Evaluate Email (2nd API Call)
    feedback = evaluate_email(email, data)
    print("\n" + "=" * 60)
    print("EVALUATION")
    print("=" * 60)
    print(feedback)

    # Step 4: Revise Email (3rd API Call)
    if should_revise(feedback):
        final_email = revise_email(email, feedback, data)
    else:
        final_email = email

    print("\n" + "=" * 60)
    print("FINAL EMAIL")
    print("=" * 60)
    print(final_email)

if __name__ == "__main__":
    main()