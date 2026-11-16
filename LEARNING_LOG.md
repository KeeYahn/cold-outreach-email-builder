# Cold Outreach Email Builder — Development & Learning Log

## Purpose of This Document

This document records the development of my Cold Outreach Email Builder, including the problems I attempted to solve, the technical decisions I made, the concepts I learned, and how my understanding of AI-powered products evolved.

The project began as an exercise in prompt engineering and in python basics, but gradually developed into a multi-stage AI workflow with structured evaluation, input validation, and conditional execution.

My primary goal was not simply to build an email generator. It was to gain practical experience designing AI-powered systems that help to address some of my real user problems while understanding aspects of product development.

## Development Overview

| Version | Theme | Central Learning Question | Status |
|---|---|---|---|
| V1.0 | Email Drafting & Prompt Engineering | How can structured user inputs guide an LLM toward a useful output? | Completed |
| V1.5 | Multi-Step Workflows & API Orchestration | How can multiple AI calls work together to improve an output? | Completed |
| V2.0 | Conditional Workflows & Decision Logic | How can a system determine whether another AI call is necessary? | Completed |
| V2.5 | Context Enrichment & Tool Calling | Can AI acquire missing information before generating an answer? | Proposed |
| V3.0 | Persistent Knowledge & RAG | How can an AI system retrieve and use information across interactions? | Proposed |
| V4.0 | Autonomous Investigation & Agents | How can an AI system plan and execute multi-step tasks using tools? | Proposed |

---

# V1.0 — CLI Email Builder: Prompt Engineering

**Theme:** Structured Inputs → Prompt Construction → AI Output

## 1. Objective

Build a Python command-line application that collects information about a sender and recipient, constructs a structured prompt, and uses the OpenAI API to generate a personalized cold outreach email.

The initial objective was to understand how Python could connect to an LLM through an API and how prompt engineering could influence the quality of the output.

## 2. Problem Being Addressed

Writing a cold outreach email involves more than putting sentences together.

The sender must identify a meaningful reason for contacting a specific recipient, find a relation point between the sender and recipient, decide which personal details are relevant, and communicate a clear learning goal without making the email overly self-focused.

Initially, I believed that the main challenge was creating a strong prompt capable of turning user inputs into a polished email.

As I developed the application, I began to recognize that the more important problem was identifying and prioritizing the strongest outreach angle that related the sender to the recipient.

This shifted my attention from simply generating text toward designing the reasoning process behind the output.

## 3. Features Implemented

- Command-line interface for collecting sender and recipient information.
- Required and optional input fields.
- Default values and basic input validation.
- Relationship-angle selection.
- Structured prompt generation using user-provided context.
- OpenAI API integration for generating an email.
- Prompt instructions for tone, length, relevance, and information selection.

The initial version also experimented with subject lines, explanations, and quality audits before later versions narrowed the output to the email itself.

### Workflow

`User Inputs → Validation & Defaults → Prompt Construction → OpenAI API → Generated Email`

## 4. Technical Concepts Learned

**Python Fundamentals**
- Functions, variables, loops, and conditional statements.
- Dictionaries for organizing user inputs.
- Passing information between functions.
- Collecting and validating terminal inputs.

**Prompt Engineering**
- Structuring prompts with clear objectives, constraints, and output formats.
- Distinguishing relevant information from unnecessary information.
- Controlling tone, length, and recipient focus.
- Using instructions to discourage unsupported claims and generic language.

**API Fundamentals**
- Understanding the relationship between a Python application and an external AI model.
- Sending prompts through an API.
- Receiving and displaying model-generated responses.
- Recognizing the difference between the application code and the LLM's generated output.

## 5. Key Takeaways

My original mental model was:

*If I can write a sufficiently good prompt, I can generate a sufficiently good email.*

By the end of V1.0, I began thinking differently.

The quality of the output depended not only on the prompt's wording, but also on which information the system selected and how it established relevance between the sender and recipient.

I began to see that the application's real value might be identifying meaningful connection points rather than merely writing emails.

This was my first shift from thinking about **AI capabilities** toward thinking about **user problems and workflow design**.

## 6. Remaining Limitations

- Sometimes included too much sender background.
- Occasionally followed the user's requested phrasing too literally.
- Output quality was inconsistent and sometimes below my custom GPT baseline.
- A single generation step provided no separate evaluation or improvement mechanism.
- Required users to provide sufficient context manually.
- Operated entirely through the terminal.

These limitations motivated the introduction of a multi-step workflow in V1.5.

---

# V1.5 — CLI Email Builder: Multi-Step AI Workflow

**Theme:** AI Generation → AI Evaluation → AI Revision

## 1. Objective

Expand the application from a single AI generation call into a multi-stage workflow in which the model could generate an email, evaluate its weaknesses, and revise the original draft.

The central question was:

*Can multiple specialized AI calls work together to produce a better result than a single generation call?*

A secondary objective was to develop a deeper understanding of API integration, Python architecture, and the flow of information between different components of an AI application.

## 2. Problem Being Addressed

Although V1.0 could produce usable emails, the quality was inconsistent.

Some drafts contained excessive sender information, weak personalization, or phrasing that could have been improved.

I wanted the system to identify these issues in a manner similar to a person reviewing their own writing.

Instead of relying entirely on the initial generation prompt, I introduced a separate evaluation stage followed by a revision stage.

This allowed the application to break a complex objective into smaller tasks.

## 3. Features Implemented

- Multiple sequential OpenAI API calls.
- Initial email generation.
- Separate evaluation of the generated email.
- Revision based on evaluator feedback.
- Distinct prompts for generation, evaluation, and revision.
- Modular separation of user input collection, prompt construction, API communication, and validation.
- API calls using both the OpenAI Python SDK and direct HTTP requests.
- HTTP request configuration, authorization headers, response parsing, and error handling.

### Workflow

`User Inputs → Validation → Generation → Evaluation → Revision → Final Email`

Unlike V2.0, the revision step was always executed, regardless of whether the original draft was already strong.

## 4. Technical Concepts Learned

**API Integration**
- Understanding the complete request-response cycle:
  `Input → Prompt → Payload → HTTP Request → API Response → Parsing → Application Logic`
- Distinguishing the OpenAI SDK from direct HTTP API requests.
- Constructing HTTP headers and request payloads.
- Using authentication credentials through environment variables.
- Handling HTTP status codes and request failures.
- Parsing nested JSON responses into Python objects.

**Python & Software Architecture**
- Organizing code across multiple Python files.
- Importing and calling functions across modules.
- Passing dictionaries and other data structures between functions.
- Working with nested dictionaries and lists.
- Using virtual environments to isolate project dependencies.
- Managing API credentials with `.env` files.
- Using exceptions to handle invalid responses and unexpected data.

**AI Workflow Design**
- Separating generation, evaluation, and revision into distinct stages.
- Using different prompts for different responsibilities.
- Passing the output of one AI call into another.
- Understanding that an AI application can involve several coordinated operations rather than a single prompt.

## 5. Key Takeaways

### Designing Constraints Around a Business Objective
One of the most important changes in my approach was moving from asking, "How do I write a good prompt?" to asking, "How do I constrain and organize an AI model to achieve a specific business objective?"

I began to understand that prompt engineering is not simply about finding the right wording. It involves defining the model's responsibilities, establishing constraints, controlling output formats, and determining which information should influence the final result.

This helped me understand the relationship between prompt design and software architecture. The prompt defines how the model should behave within a particular task, while the surrounding application determines how that task fits into the broader workflow.

V1.5 significantly changed my mental model of AI development.

Previously, I thought about AI applications primarily as prompts connected to models.

After building a multi-step workflow, I began viewing an AI application as a system of interconnected components:

`Input Layer → Validation → Prompt Construction → AI Generation → AI Evaluation → AI Revision → Output`

I also began thinking more about product design.

Instead of asking only, *"Can ChatGPT write a good email?"* I began asking, *"What friction does a user experience when trying to write a good outreach email, and which parts of that process should the system handle?"*

This introduced me to a more structured way of approaching AI product development: designing workflows around problems rather than adding AI capabilities for their own sake.

## 6. Remaining Limitations

- The evaluation and revision stages sometimes made only minor improvements.
- Occasionally, the revised email was weaker than the original.
- The application always made a third API call, even when the initial draft was already strong.
- Unnecessary revisions increased token consumption, latency, and potential API costs.
- Evaluation feedback was not yet structured for deterministic decision-making.
- The application still relied on user-provided context without external research.

These limitations motivated V2.0: introducing conditional logic to determine whether revision was necessary.

---

# V2.0 — CLI Email Builder: Conditional AI Workflow

**Theme:** Structured Evaluation → Deterministic Decision-Making → Conditional Execution

## 1. Objective

Improve the efficiency and reliability of the email generation workflow by introducing a decision-making layer between evaluation and revision.

Instead of automatically revising every draft, the system would assess the initial email and determine whether revision was likely to be useful.

The central question was:

*How can an AI system use model-generated judgments without giving the model complete control over the application's behavior?*

This version focused on structured outputs, conditional execution, factual consistency, and testing.

## 2. Problem Being Addressed

The primary weakness of V1.5 was that the workflow was linear.

Every generated email passed through all three API calls:

1. Generation.
2. Evaluation.
3. Revision.

This created two problems.

**Unnecessary API usage:** Strong initial drafts were still sent through another model call, increasing latency and token costs without necessarily improving the output.

**Unreliable revision quality:** The evaluator could suggest changes even when the original email was already effective. The revision stage sometimes altered strong wording or introduced unnecessary modifications.

A secondary concern was factual accuracy.

Because cold outreach emails depend on personal backgrounds and relationships, invented connections, achievements, referrals, or experiences could damage the sender's credibility.

I wanted the system to treat unsupported factual claims as a higher-priority problem than ordinary stylistic weaknesses.

## 3. Features Implemented

### A. Structured JSON Evaluation

Reworked the evaluation prompt so the model returns a structured JSON object rather than unstructured written feedback.

The evaluation includes:

```json
{
  "overall_score": 8,
  "revision_recommended": false,
  "issue_type": "none",
  "weaknesses": [],
  "reason": "The email is sufficiently specific and concise."
}
```

Each field serves a distinct purpose:

- `overall_score`: Numerical quality assessment from 1–10.
- `revision_recommended`: Boolean indicating whether the evaluator recommends revision.
- `issue_type`: The primary issue identified.
- `weaknesses`: List of specific weaknesses.
- `reason`: Explanation of the evaluation.

This structure makes the evaluator's output usable by Python code.

### B. Deterministic Revision Decision Tree

Introduced the `should_revise()` function to decide whether the application should make another API call.

The current rules are:

1. **Misrepresentation:** Always revise when the evaluator identifies misrepresentation.
2. **Low quality score:** Revise when the overall score is below 8.
3. **Substantive recommendation:** Revise when the evaluator recommends revision and identifies an issue other than `none`.
4. **Otherwise:** Preserve the original email.

This means a score of 8 does not automatically trigger revision, although revision may still occur under the other conditions.

The key architectural change was separating the evaluator's recommendation from the application's final decision.

### C. Evaluation Response Parsing & Validation

Expanded `ai_client.py` to extract and validate the structured evaluation response.

The program now checks:

- Whether the response contains a message with text.
- Whether the returned text is valid JSON.
- Whether the parsed JSON is a dictionary.
- Whether all required fields are present.
- Whether the score is numeric, not Boolean, and between 1–10.
- Whether `revision_recommended` is a Boolean.
- Whether `issue_type` belongs to the allowed categories.
- Whether `weaknesses` is a list of strings.
- Whether `reason` is a string.

Invalid responses raise errors rather than being passed directly into the decision tree.

This reduces the risk of malformed model output causing incorrect downstream behavior.

### D. Factual Consistency & Misrepresentation Detection

Updated the evaluation and revision prompts to include the original user-provided context.

The evaluator is instructed to compare factual claims in the email against that context and flag unsupported claims as `misrepresentation`.

The revision prompt is instructed to preserve supported details and avoid introducing new factual claims.

This provides an additional safeguard against fabricated relationships, referrals, achievements, or other personal details.

The checks are model-based, however, and do not independently verify facts against external sources.

### E. Conditional Workflow Execution

Changed the application so revision is optional.

### Updated Workflow

```text
User Inputs
    |
    v
Validation & Defaults
    |
    v
Prompt Construction
    |
    v
AI Generation
    |
    v
AI Evaluation (JSON)
    |
    v
Parse & Validate Evaluation
    |
    v
Python Decision Tree
    |
    +---- Should Revise? ----+
    |                       |
   Yes                      No
    |                       |
    v                       |
AI Revision                 |
    |                       |
    +-----------+-----------+
                |
                v
            Final Email
```

A successful workflow now requires two API calls when revision is unnecessary and three when revision is required.

### F. Testing & Debugging

Added and executed tests covering the decision tree, malformed JSON handling, and factual misrepresentation.

Testing included:

- Six decision-tree test cases.
- Malformed JSON parsing behavior.
- An adversarial evaluation containing fabricated personal connections.
- End-to-end generation and evaluation.
- Cases where the original draft was preserved.
- Cases where revision was triggered.
- Python syntax checks using `py_compile`.

The adversarial evaluation test identified fabricated relationship claims and classified them as misrepresentation.

These tests increased confidence in the implemented logic, although they do not establish production-level reliability.

## 4. Technical Concepts Learned

**Structured Outputs & Data Validation**
- Difference between JSON text and Python dictionaries.
- Converting JSON strings into Python objects using `json.loads()`.
- Validating required dictionary keys and value types.
- Handling malformed JSON using exceptions.
- Recognizing that successful parsing does not guarantee valid data.
- Understanding Python's treatment of Booleans as a subclass of integers and why numeric validation may need to reject them explicitly.

**Conditional Logic & System Design**
- Moving from a fixed sequence of operations to conditional execution.
- Designing decision trees using Python.
- Separating model-generated judgments from deterministic application rules.
- Understanding when an AI model should evaluate a situation versus when application code should make the final decision.
- Recognizing that additional AI calls are not always beneficial.

**Reliability & Error Handling**
- Using `try`/`except` blocks to handle parsing failures.
- Distinguishing syntax errors, type errors, and invalid data.
- Using explicit validation before passing model output into downstream functions.
- Testing failure scenarios rather than only successful outputs.
- Recognizing that AI-generated factual checks can themselves be incorrect.

**Testing & Debugging**
- Writing unit tests for isolated decision logic.
- Testing expected outcomes across multiple scenarios.
- Understanding the purpose of breakpoints and step-by-step debugging.
- Using `py_compile` to check syntax without executing the application.
- Distinguishing unit tests from end-to-end application testing.
- Understanding how virtual environments affect Python execution and installed dependencies.

**Efficiency & Product Engineering**
- Understanding the relationship between API calls, token consumption, latency, and cost.
- Identifying unnecessary workflow steps.
- Preserving strong outputs rather than modifying them automatically.
- Designing around the expected value of an additional AI call rather than assuming more model calls always produce better results.

## 5. Key Takeaways

### A. Choosing Between AI Judgment and Deterministic Logic

One of the most important architectural lessons from V2.0 was learning that not every decision within an AI-powered application needs to be made by an LLM.

In V1.5, the model evaluated the initial email, but the application automatically proceeded to revision regardless of the evaluation. In V2.0, I separated the model's evaluation from the application's execution logic, allowing the system to determine whether revision was actually necessary.

This introduced an important distinction between two types of responsibilities:

- **AI (Probabilistic Judgment):** Evaluates subjective qualities such as personalization, clarity, relevance, and overall email quality. It identifies weaknesses and recommends whether revision would be beneficial.
- **Python (Deterministic Logic):** Validates the evaluation response, applies predefined conditions, and determines whether the revision stage should execute.

This separation offered several advantages:

- **Predictability:** Given the same validated evaluation, the decision tree produces the same result.
- **Control:** I can modify revision thresholds and conditions without changing the evaluator's prompt.
- **Testability:** I can test the decision-making logic independently without making API calls.
- **Efficiency:** The application can avoid unnecessary revision calls when the original draft is already strong.

The broader lesson was that building an AI-powered system does not mean delegating every task or decision to AI. Traditional programming can provide greater reliability, transparency, and control when the decision criteria are clearly defined.

I began to recognize that an important part of AI system design is determining **where probabilistic AI judgment adds value and where deterministic application logic is more appropriate.**

### B. More AI Calls Do Not Necessarily Mean Better Results

Initially, adding evaluation and revision seemed like an obvious improvement over generating a single draft.

However, testing showed that revisions were not consistently better.

This highlighted the importance of measuring whether an additional step provides enough value to justify its cost and complexity.

The objective should not be to maximize the number of AI operations, but to use them selectively when they improve the outcome.

### C. Model Outputs Should Be Treated as Untrusted Data

An LLM can return malformed JSON, unexpected types, unsupported factual claims, or inconsistent evaluations.

Even when the prompt clearly specifies the desired format, the application should not assume that every response will be valid.

V2.0 introduced a more disciplined approach:

`Model Response → Parsing → Validation → Decision Logic → Execution`

This was an important step toward understanding reliability in AI systems.

### D. Testing Includes Deliberately Trying to Break the System

Earlier development focused heavily on whether the program could produce a good email.

In V2.0, I began testing what happened when the evaluator returned invalid data or when an email contained fabricated information.

This introduced the distinction between demonstrating that a feature works under normal conditions and testing how it behaves when assumptions fail.

### E. The Bottleneck May Exist Before Generation

Even after improving the generation and revision workflow, a major source of friction remained: users still had to supply detailed, high-quality context.

The system could organize and rewrite information, but it could not independently discover the strongest reasons to contact someone.

This suggested that the next meaningful improvement might involve information acquisition rather than additional prompt refinement.

## 6. Remaining Limitations

- The evaluator's scores and recommendations are subjective and may vary between runs.
- The decision threshold of 8 is a heuristic rather than an empirically optimized value.
- Misrepresentation detection compares claims against supplied context; it does not independently verify real-world facts.
- The application cannot guarantee that a revised draft is better than the original.
- No systematic benchmarking has been conducted across a large dataset of outreach emails.
- The application does not independently research recipients or gather missing information.
- User input remains relatively time-consuming.
- The application has no persistent memory, database, or graphical interface.
- API response handling is sufficient for tested cases but not exhaustive across all possible response structures.
- The application remains a local learning project rather than a production-ready product.

These limitations provide potential directions for future development, but V2.0 is considered complete.

---

# Future Exploration — Proposed Versions

The following versions represent possible extensions of the project, not completed implementations.

The current plan is to apply new AI engineering concepts to a separate Product Analytics Copilot rather than necessarily continue expanding the email builder.

## V2.5 — Context Enrichment & Tool Calling

**Theme:** Acquiring Information Before Generation

### Objective

Explore whether an AI application can improve weak user inputs by retrieving additional information from external sources.

**Central question:** *Can AI acquire missing information before reasoning and generation?*

### Problem Being Addressed

Even a well-designed generation workflow depends on the quality of its inputs.

Users may struggle to identify meaningful relationship angles or explain why a particular recipient is relevant.

An application that can retrieve publicly available recipient or company information could reduce this friction.

### Proposed Features

- Detect missing or weak context.
- Use external APIs or search tools to gather relevant information.
- Identify possible outreach angles based on retrieved information.
- Present suggested connections for user review.
- Generate emails using confirmed information.
- Preserve the existing evaluation and conditional revision workflow.

### Proposed Workflow

`User Inputs → Context Assessment → Tool Calling → Information Retrieval → User Review → Generation → Evaluation → Conditional Revision → Final Email`

### Concepts to Explore

- Tool/function calling.
- External APIs and information retrieval.
- Data provenance and source reliability.
- Human-in-the-loop approval.
- Handling incomplete or conflicting external information.

### Key Hypothesis

Improving the information available before generation may create more value than adding additional rewriting stages afterward.

---

## V3.0 — Persistent Knowledge & Retrieval-Augmented Generation

**Theme:** Using Stored Information Across Interactions

### Objective

Explore how an AI application can retrieve relevant information from a persistent knowledge base rather than relying entirely on information entered during each session.

**Central question:** *How can AI use previously stored information without requiring users to repeat it?*

### Potential Applications

- Storing recipient profiles and previous interactions.
- Retrieving notes from earlier networking conversations.
- Using past correspondence to personalize follow-ups.
- Supporting preparation for future conversations.

### Concepts to Explore

- Retrieval-Augmented Generation (RAG).
- Embeddings and semantic search.
- Vector databases.
- Persistent storage and data retrieval.
- Context selection and relevance.
- Privacy and data management.

### Key Hypothesis

A useful networking assistant may eventually need to manage relationships and accumulated knowledge, not just generate individual emails.

---

## V4.0 — Autonomous Investigation & AI Agents

**Theme:** Planning and Executing Multi-Step Tasks

### Objective

Explore how an AI system can plan and coordinate multiple tool-based actions toward a larger objective.

**Central question:** *When should an AI system be allowed to determine its own sequence of actions rather than follow a predefined workflow?*

### Potential Applications

- Researching a recipient and their company.
- Identifying relevant professional connections.
- Preparing conversation briefs.
- Suggesting follow-up actions.
- Coordinating information retrieval, evaluation, and drafting.

### Concepts to Explore

- Agentic workflows.
- Planning and tool selection.
- Multi-step execution.
- State management.
- Human oversight and approval.
- Error recovery and stopping conditions.

### Key Hypothesis

Greater autonomy may improve flexibility, but it also introduces complexity, reliability concerns, and additional costs. An autonomous system should be justified by the task rather than implemented simply because agentic capabilities are available.

---

# Overall Reflection

The most significant progression throughout this project was a change in how I conceptualized AI-powered software.

**V1.0:** I focused on creating a prompt that could generate a useful output.

**V1.5:** I learned to design a workflow involving multiple specialized AI calls.

**V2.0:** I learned to separate model-generated judgments from application-controlled decisions, validate model outputs, and selectively execute expensive operations.

The broader shift was from asking:

*"How can I make the AI produce a better answer?"*

to asking:

*"How should I design a reliable, efficient system that uses AI to solve a specific user problem?"*

The project also highlighted an important product lesson: improving the technical workflow does not necessarily solve the user's largest problem. In this case, the difficulty of finding a meaningful outreach angle and gathering relevant context may matter more than the quality of the final email's wording.

The next step in my learning journey is to apply these concepts to a Product Analytics Copilot, with a greater emphasis on data retrieval, tool calling, analytical workflows, and the reliability of AI-assisted decisions.