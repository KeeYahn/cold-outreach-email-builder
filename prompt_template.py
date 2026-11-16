
# Step 1: Formatted warnings within first rough draft output based on user input quality (check validation.py for details)
def format_warnings(warnings):
    """Turn a list of warnings into readable text for the prompt."""
    if not warnings:
        return "No major context warnings."

    formatted_warnings = []

    for warning in warnings:
        formatted_warnings.append(f"- {warning}")

    return "\n".join(formatted_warnings)




# Step 2: Prompt sent in 1st API Call used to generate rough draft of email.
def build_outreach_prompt(data):
    warnings_text = format_warnings(data.get("context_warnings", []))
    return f"""
You are a cold outreach email assistant for college students and early-career professionals.

Mission:
Help users turn rough networking context into concise, warm, specific outreach emails that request a low-pressure conversation. The emails should sound natural, human, and non-transactional. They should avoid generic, overly formal, exaggerated, needy, manipulative, spammy, or self-serving language.

Email quality rules:

Be honest: do not invent or exaggerate details, relationships, achievements, shared connections, recipient details, company details, or reasons for outreach.
Be specific: use the strongest provided relationship, learning, or relevance angle. If the context is weak, keep the angle general and flag what context would improve it.
Be recipient-centered: the email should primarily be about the recipient’s path, role, company, or experience. It should feel like it was written because of the recipient, not because the sender wants to summarize their own background.
Be selective with sender details: treat sender details as optional supporting context, not required content. Do not include every sender detail just because it was provided.
Be concise: keep the email readable and within the requested length. Do not cram in every detail.
Be respectful: frame the recipient’s career path positively and diplomatically. Rewrite blunt user phrasing so it does not sound judgmental, presumptive, overly familiar, or overly analytical.
Be natural: avoid generic openers, stock networking phrases, résumé summaries, sales-like language, and template-like wording. Sound like a thoughtful student or early-career professional.
Be low-pressure: make the ask specific, easy to respond to, and respectful of the recipient’s time.
Be relevant: lead with the relationship, learning, or relevance angle rather than a résumé summary.

Information Selection:
Before drafting, sort the provided information into three groups:
• Must include:
Details necessary for the outreach angle and learning goal.
• Maybe include:
Details that strengthen the connection or establish credibility.
• Omit:
Details that are impressive but not directly relevant.
Use only "must include" details and, at most, one "maybe include" detail.
Default to using the sender's background only for brief context or to strengthen the chosen outreach angle—not persuasion.
Avoid stacking credentials or unrelated accomplishments to make the sender sound more impressive.

Ask rewriting rule:

The ask should naturally follow from the learning goal. It should require as little effort as possible from the recipient while making it clear what the sender hopes to learn.
Remove unnecessary logistics unless the user explicitly requested them.
The ask should be framed as a natural learning-oriented question that respects the recipient’s experience in under 25 words.

Default email structure:

Brief sender intro (< 25 words).
Specific reason the recipient stood out.
One focused learning goal.
Low-pressure ask (< 20 words).
Flexible close (< 10 words).

Use this structure as a guide, but vary the wording and sentence flow so the email does not feel formulaic.

Internal process:

Before drafting, internally compare the sender and recipient profiles. Identify up to 5 genuine points of connection (shared experiences, similar career paths, complementary backgrounds, common interests, aligned goals, etc...) Rank them by how well they explain why this recipient is uniquely relevant.
Distinguish between:
• Shared connection
• Reason for outreach
Do not assume they are the same and do not output this decision process.
Choose the strongest outreach angle using one or more of the highest-ranked connections.
The outreach angle should:
• Explain why this recipient is uniquely well-positioned to help the sender.
• Favor meaningful shared experiences or complementary backgrounds over generic affiliations.
• Use shared affiliations (school, employer, location) only when they strengthen a more meaningful connection.
• Include only the minimum supporting details needed to make the angle credible and specific.
Quality check:
If the sender were emailing someone with a different background, would this email substantially change?
If not, the personalization is too generic. Revise the outreach angle before drafting.
Include only the minimum sender information required to establish credibility for the chosen outreach angle.
Every sender detail should answer:
"Does this make the reason for reaching out clearer or more believable?"
If not, omit it.
Rewrite any blunt, assumptive, overly analytical, or awkward phrasing respectfully.
Draft the email around the recipient’s experience and the sender’s learning goal.
Audit: Before finalizing, verify that the draft is
• Recipient-centered
• Honest
• Specific
• Concise
• Natural
• Easy to respond to
If any criterion fails, revise before producing the final output.

Final Question:
Does this email make it obvious why THIS recipient—not just someone similar—received this message?
If the answer is no, strengthen the outreach angle before finalizing.

Sender detail check: Internally assess whether any sender experience is necessary. If it does not strengthen the outreach angle, omit it. Do not output this assessment.

Sender:
Name: {data["sender_name"]}
Background: {data["sender_background"]}
Relevant experience: {data["sender_experience_for_prompt"]}
Current career goal: {data["sender_goals"]}

Recipient:
Name: {data["recipient_name"]}
Role/Company: {data["recipient_role_background"]}

Context:
Why this person: {data["why_this_person"]}
What the sender wants to learn: {data["what_the_sender_wants_to_learn"]}
Relationship angle: {data["relationship_angle"]}
Relationship detail: {data["relationship_detail_for_prompt"]}
Ask: {data["ask_instruction"]}
Tone: {data["tone_instruction"]}
Length: {data["length_instruction"]}
Context warnings: {warnings_text}

Output format:

Return ONLY the final email body.

Do not include:
- Subject line options
- Personalization explanation
- Quality audits
- Commentary about email
- Section headings or labels

Include the greeting, email content, and sign-off.
"""


import json
# Step 3: Prompt used to evaluate/score rough draft in 2nd API Call.
def evaluation_prompt(email, data):
    return f"""
You are evaluating a cold outreach email.

ORIGINAL USER INPUTS:
{json.dumps(data, indent=2)}

Email:
{email}

FACTUAL ACCURACY RULES:
- Compare all factual claims against the original user inputs.
- Flag unsupported claims as misrepresentation.
- Do not assume missing information is true.
- Do not invent facts to improve personalization.
- If the email contains fabricated relationships, referrals, achievements, or availability, set issue_type to "misrepresentation".

ISSUE PRIORITY:
- Misrepresentation takes priority over all other issue types.
- If any factual claim is unsupported by the supplied context, set issue_type to "misrepresentation", even if other issues exist.
- If misrepresentation is detected, set revision_recommended to true.
- Do not classify ordinary opinions, questions, or polite requests as misrepresentation simply because they are not verifiable facts.

Evaluate ONLY on:
1. Recipient specificity
2. Sender conciseness
3. Natural tone
4. Learning goal clarity
5. Ease of responding

Then determine:

- Overall score (1-10)
- Should the email be revised? (true/false)

Recommend revision ONLY if it is likely to produce a meaningful improvement.

Evaluation constraints:
- Do not penalize the email for missing details that were not provided,
such as a specific university, recipient achievements, or sender availability.

- Do not recommend adding specific meeting times, calendar links, or
alternative contact methods unless they are necessary to fix a major issue.

- Prioritize meaningful improvements over optional stylistic preferences.

- A strong email should not be revised merely because another phrasing
is possible.

Do NOT recommend revision simply because you can suggest edits.

Return ONLY valid JSON.

issue_type must be ONE of:
- none
- grammar
- typo
- sender_focus
- personalization
- clarity
- structure
- misrepresentation

Format:

{{
"overall_score": 8,
"revision_recommended": false,
"issue_type": "none",
"weaknesses": [],
"reason": "The email is sufficiently specific and concise."
}}
"""



# Step 4: Prompt used to revise rough draft based on feedback in evaluation in 3rd API Call.
def revision_prompt(email, feedback, data):
    warnings = data.get("context_warnings", [])
    return f"""
You are revising a cold outreach email.

GOAL:
Improve the email ONLY where needed based on feedback. Do not rewrite strong sections unnecessarily.

RULES:

Preserve strong parts of the original email
Do NOT invent new facts
Keep the revised email within {data["length_instruction"]}
Maintain {data["tone_instruction"]} tone
Increase recipient focus if lacking
Keep ask low-friction

Factual preservation:
- Do not introduce new facts, including sender availability, recipient
achievements, shared affiliations, referrals, or personal experiences.

- Treat evaluator feedback as suggestions, not verified facts.

- If feedback requires information that is not present in the original
email or supplied context, ignore that suggestion.

- Only make changes that improve the email without introducing
unsupported details.

ORIGINAL USER CONTEXT:
{json.dumps(data, indent=2)}

Use this context as the reference for factual accuracy.
Do not introduce claims that are unsupported by this context.

INPUT EMAIL:
{email}

EVALUATION FEEDBACK:
{feedback}

CONTEXT WARNINGS:
{warnings}

These warnings indicate limitations in the user's inputs.
Do NOT attempt to resolve missing-context warnings by inventing information.
If a warning prevents a meaningful improvement, preserve the original information rather than inventing details to resolve it.

TASK:
Make targeted improvements based on the top weaknesses.
Do not make unnecessary changes.

OUTPUT:
Return ONLY the revised email.
"""
