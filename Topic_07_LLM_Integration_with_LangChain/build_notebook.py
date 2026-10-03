"""Builds 07_LLM_Integration_with_LangChain.ipynb.

Unlike Topic 6's build_notebook.py, this notebook is NOT auto-executed end-to-end
during the build. It calls a live LLM API (Google Gemini via langchain-google-genai),
which requires a personal, free API key that must never be hardcoded or embedded in
this repository. The instructor should run the notebook once, top to bottom, with
their own key (see README.md) before teaching, to confirm outputs before class.
"""
import nbformat as nbf
import os

nb = nbf.v4.new_notebook()
cells = []


def md(text):
    cells.append(nbf.v4.new_markdown_cell(text))


def code(text):
    cells.append(nbf.v4.new_code_cell(text))


# ============================================================
# PART 1: INTRODUCTION
# ============================================================
md("""# LLM Integration with LangChain
### Topic 7 — Introduction to Large Language Models

## What Are We Building?

By the end of this hour you will have built a **Simple Customer Support Assistant**
for a fictional microfinance bank, using this flow:

```
User Question -> Prompt Template -> LLM -> Response
```

This is the simplest possible shape of an LLM application, and it is the foundation
every more advanced LangChain pattern (chains, RAG, agents) is built on top of.

## Learning Objectives
By the end of this notebook, you will be able to:
- Install and import the required LangChain packages.
- Configure access to an LLM safely, without hardcoding an API key.
- Create a prompt template and pass user input into it.
- Send a prompt to an LLM and read the response.
- Build a small reusable function that wraps a prompt + LLM chain.
- Modify a prompt and observe how the response changes.
- Provide extra context to the LLM and see how it changes the answer.
- Understand, conceptually, how this connects to Retrieval-Augmented Generation (RAG).

## Central Example
Throughout this notebook, we pretend we work for a **microfinance bank** that wants an
AI assistant to answer customer questions such as *"How do I apply for a loan?"* or
*"What happens if I miss a repayment?"*. All bank information used here is **synthetic**
— invented purely for teaching.
""")

# ============================================================
# PART 2: INSTALL AND IMPORT PACKAGES
# ============================================================
md("""## 1. Install the Required Packages

We use **Google Gemini** as our LLM in this course because it has a genuinely free
API tier, is well documented, and is easy to set up in Google Colab — no credit card
required to follow along.

- `langchain` and `langchain-core` — the framework: prompt templates, chains, output parsers.
- `langchain-google-genai` — the official LangChain integration for Google's Gemini models.

If you later want to use a different provider (e.g. OpenAI), only this integration
package and the model-configuration cell below would need to change — everything else
in this notebook (prompt templates, chains, the reusable function) stays the same.
""")

code("""!pip install -qU langchain langchain-core langchain-google-genai
""")

code("""from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

print("Imports successful.")
""")

# ============================================================
# PART 3: CONFIGURE THE LLM
# ============================================================
md("""## 2. Configure Access to the LLM

**Never write your API key directly into a notebook cell or a script.** Anyone who
sees the file (or if you accidentally push it to GitHub) could then use your key.

Instead, this notebook supports two safe ways to provide your key:

1. **Google Colab Secrets** (recommended in Colab): click the key icon in the left
   sidebar, add a secret named `GOOGLE_API_KEY` with your key as the value, and grant
   this notebook access to it.
2. **`getpass`** (works anywhere, including outside Colab): the cell below will
   securely prompt you to type your key without displaying it on screen, if no Colab
   secret is found.

Get a free key from **Google AI Studio** (https://aistudio.google.com/apikey) before
running the cell below.
""")

code("""import os

api_key = None

# Try Colab Secrets first
try:
    from google.colab import userdata
    api_key = userdata.get("GOOGLE_API_KEY")
except Exception:
    pass

# Fall back to a secure manual prompt
if not api_key:
    import getpass
    api_key = getpass.getpass("Enter your Google AI Studio API key: ")

os.environ["GOOGLE_API_KEY"] = api_key
print("API key configured.")
""")

md("""### Choosing a Model

We use `"gemini-flash-latest"` — an alias that always points at Google's current,
free-tier "Flash" model, so this notebook keeps working even after Google releases
newer model versions.

`temperature` controls how random/creative the output is:
- Lower (e.g. `0.0`-`0.3`) -> more focused, consistent, repeatable answers. Good for
  customer support, where we want reliable answers rather than creative ones.
- Higher (e.g. `0.8`-`1.0`) -> more varied, creative answers. Good for brainstorming
  or creative writing, less appropriate for a support assistant.
""")

code("""llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    temperature=0.3,   # low temperature: consistent, focused answers for customer support
)

print("LLM configured:", llm.model)
""")

# ============================================================
# PART 4: FIRST LLM CALL
# ============================================================
md("""## 3. Your First LLM Call

Let's make the simplest possible call: ask the model one question directly, with no
template and no extra structure yet.

### Interpretation
`llm.invoke(text)` sends `text` to the model and returns a message object.
`.content` holds the generated text. This is the `Input -> Model -> Output` pattern
from the slides, in three lines of code.
""")

code("""response = llm.invoke(
    "Explain what a microfinance loan is to a new customer in simple language."
)
print(response.content)
""")

md("""**Trainer Question:** Look at the response above. Is it written in language a
first-time bank customer (not a finance expert) could understand? What would you
change about the instruction to make it more suitable for our bank's use case?
""")

# ============================================================
# PART 5: PROMPT ENGINEERING BASICS
# ============================================================
md("""## 4. Prompt Engineering Basics

Small changes in how you phrase an instruction can noticeably change the model's
output. Let's compare three versions of essentially the same request, going from
vague to well-structured (Role + Task + Context + Output).
""")

code("""# Prompt 1: vague
response_1 = llm.invoke("Explain loans.")
print("--- PROMPT 1 ---")
print(response_1.content)
""")

code("""# Prompt 2: adds audience and context
response_2 = llm.invoke(
    "Explain a microfinance loan to a first-time borrower in Nigeria using simple language."
)
print("--- PROMPT 2 ---")
print(response_2.content)
""")

code("""# Prompt 3: adds role, audience, context, AND an output constraint
response_3 = llm.invoke(
    "You are a customer support assistant for a microfinance bank. Explain a "
    "microfinance loan to a first-time borrower in Nigeria using simple language. "
    "Keep the answer below 100 words."
)
print("--- PROMPT 3 ---")
print(response_3.content)
""")

md("""**Trainer Question:** Compare the three responses above. Which one is most
usable directly inside a real customer support chat window, and why?

**Common misunderstanding:** a longer prompt is not automatically a better prompt —
what matters is including the *right* pieces (role, audience, output constraints),
not sheer length.
""")

# ============================================================
# PART 6: PROMPT TEMPLATES
# ============================================================
md("""## 5. Prompt Templates

Retyping the full instruction for every customer question does not scale. A
**prompt template** lets us write the instruction once, with a placeholder for the
part that changes.

`{question}` is a variable. `ChatPromptTemplate.from_template(...)` builds a
reusable template object; `.invoke({...})` fills in the variable(s).
""")

code("""support_template = ChatPromptTemplate.from_template(
    "You are a customer support assistant for a microfinance bank.\\n\\n"
    "Customer question:\\n{question}\\n\\n"
    "Answer in simple language. If the information is not available, say that you "
    "do not have enough information."
)

# Preview what the template produces for one question, before sending it anywhere
filled_prompt = support_template.invoke({"question": "How do I apply for a loan?"})
print(filled_prompt.to_string())
""")

md("""### Interpretation
Notice the printed text above is the *finished* prompt — the template with
`{question}` replaced. This is exactly what gets sent to the LLM next.
""")

# ============================================================
# PART 7: BUILD A LANGCHAIN CHAIN
# ============================================================
md("""## 6. Building a Simple LangChain Chain

Now we connect the pieces with LangChain's pipe operator `|`, which is called LCEL
(LangChain Expression Language). Each step's output becomes the next step's input:

```
Prompt Template  |  LLM  |  Output Parser
```

- `support_template` fills in `{question}`.
- `llm` generates a response.
- `StrOutputParser()` extracts just the plain text string from the response, instead
  of the full message object.
""")

code("""support_chain = support_template | llm | StrOutputParser()

answer = support_chain.invoke({"question": "How do I apply for a loan?"})
print(answer)
""")

md("""**Trainer Question:** Compare `answer` above (a plain string) to `response.content`
from Part 4. What did adding `StrOutputParser()` change?
""")

# ============================================================
# PART 8: REUSABLE FUNCTION
# ============================================================
md("""## 7. Building a Reusable Function

Let's wrap the chain in a function so the rest of our (imagined) application can
simply call `ask_customer_support(question)` without knowing anything about prompts
or chains.
""")

code("""def ask_customer_support(question: str) -> str:
    \"\"\"Send a customer question through the support chain and return the answer.\"\"\"
    return support_chain.invoke({"question": question})


# Test it with five different customer questions
test_questions = [
    "How do I apply for a loan?",
    "What documents do I need?",
    "How can I repay my loan?",
    "What happens if I miss a payment?",
    "How do I reset my account?",
]

for q in test_questions:
    print("Q:", q)
    print("A:", ask_customer_support(q))
    print("-" * 60)
""")

md("""**Trainer Question:** All five answers above came from the *same* prompt template
and the *same* function. What does that tell you about why templates and reusable
functions matter as an application grows to handle hundreds of different questions?
""")

# ============================================================
# PART 9: ADD CONTEXT
# ============================================================
md("""## 8. Adding Context to the LLM

So far the model has answered purely from what it learned during training. Real bank
policies are specific and can change — the model cannot know them unless we give
them to it. Let's compare answering **without** context to answering **with** context.
""")

code("""tricky_question = "What are the requirements for the business loan?"

# Without context: the model can only guess generically
print("--- WITHOUT CONTEXT ---")
print(ask_customer_support(tricky_question))
""")

code("""# A short, synthetic bank policy document (invented for teaching purposes only)
business_loan_policy = \"\"\"
Business Loan Policy (Synthetic Example):
- Applicants must have an active business registered for at least 6 months.
- Applicants must provide 3 months of bank statements.
- Applicants must provide a valid government-issued ID.
- Maximum loan amount for first-time business borrowers is 500,000 NGN.
- Loans are repaid over 6 to 12 months in equal monthly instalments.
\"\"\"

context_template = ChatPromptTemplate.from_template(
    "You are a customer support assistant for a microfinance bank.\\n\\n"
    "Use ONLY the policy information below to answer the customer's question. "
    "If the answer is not in the policy information, say you do not have enough "
    "information rather than guessing.\\n\\n"
    "Policy information:\\n{context}\\n\\n"
    "Customer question:\\n{question}\\n\\n"
    "Answer in simple language."
)

context_chain = context_template | llm | StrOutputParser()

print("--- WITH CONTEXT ---")
print(context_chain.invoke({
    "context": business_loan_policy,
    "question": tricky_question,
}))
""")

md("""### Interpretation
Compare the two answers above. The "with context" answer should closely match the
specific, synthetic policy we supplied, instead of a generic, made-up description.

This is the basic idea behind giving an LLM external information — and it is exactly
the mechanism RAG automates at a larger scale.
""")

# ============================================================
# PART 10: RAG, CONCEPTUALLY
# ============================================================
md("""## 9. RAG: The Conceptual Bridge

We are **not** building a vector database in this hour — that is more than a beginner
session can responsibly fit, and it belongs in a later, dedicated session. Instead,
notice what we just did by hand:

```
Question -> Find relevant information -> Add information to prompt -> LLM -> Answer
```

In Part 8, *we* manually picked which policy text was "relevant" and pasted it into
the prompt. In a production **RAG (Retrieval-Augmented Generation)** system, that
"find relevant information" step is automated: documents are broken into chunks,
converted into numerical **embeddings**, stored in a **vector database**, and the
most relevant chunks are retrieved automatically for each question — instead of a
human choosing them by hand.

The mechanism you just used (give the LLM the right information before asking for an
answer) is the same core idea. RAG just automates the *finding* step at scale.
""")

# ============================================================
# PART 11: EXERCISES
# ============================================================
md("""## 10. Exercises

Try each exercise yourself before checking the solution underneath it.

### Exercise 1 — Improve the Prompt
The prompt below is weak. Rewrite it using the Role + Task + Context + Output
structure from the slides, then run it and compare the two answers.

```python
weak_prompt = "Tell me about repayment."
```
""")

code("""# Exercise 1: your improved prompt (edit this)
weak_prompt = "Tell me about repayment."
print(llm.invoke(weak_prompt).content)
""")

code("""# Your improved version here
# improved_prompt = "..."
# print(llm.invoke(improved_prompt).content)
""")

md("""**Solution 1**
```python
improved_prompt = (
    "You are a customer support assistant for a microfinance bank. "
    "Explain to a customer, in simple language, the different ways they can repay "
    "their loan. Answer in 3 short bullet points."
)
print(llm.invoke(improved_prompt).content)
```
Adding a role, a specific audience, and an output format (3 bullet points) typically
produces a noticeably more usable answer than the one-line original.
""")

md("""### Exercise 2 — Change the Response Format
Ask the model to answer the same question three ways: as bullet points, as a short
paragraph, and as a small table. Notice that only the *output format instruction*
changes between the three prompts.
""")

code("""# Your code here for the three formats
""")

md("""**Solution 2**
```python
base_q = "What documents do I need to apply for a loan?"

print(llm.invoke(f"{base_q} Answer as bullet points.").content)
print(llm.invoke(f"{base_q} Answer as a short paragraph.").content)
print(llm.invoke(f"{base_q} Answer as a small markdown table with columns Document and Why it's needed.").content)
```
""")

md("""### Exercise 3 — Build a Reusable Function
Modify `ask_customer_support` (or write a new function `ask_in_style`) so it accepts
a second argument, `style`, and includes it in the prompt (e.g. `"formal"`,
`"friendly"`, `"very short"`).
""")

code("""# Your code here
""")

md("""**Solution 3**
```python
style_template = ChatPromptTemplate.from_template(
    "You are a customer support assistant for a microfinance bank.\\n\\n"
    "Customer question:\\n{question}\\n\\n"
    "Answer in simple language, using a {style} tone."
)
style_chain = style_template | llm | StrOutputParser()

def ask_in_style(question: str, style: str) -> str:
    return style_chain.invoke({"question": question, "style": style})

print(ask_in_style("How do I reset my account?", "friendly"))
print(ask_in_style("How do I reset my account?", "very formal"))
```
""")

md("""### Exercise 4 — Add Context
Below is a new, short synthetic policy. Write a prompt (or reuse `context_chain`
from Part 8) so the model answers the question **using only** this policy.

```python
repayment_policy = \"\"\"
Repayment Policy (Synthetic Example):
- Repayments are due on the 5th of every month.
- A grace period of 3 days is given before a late fee applies.
- Missing 2 consecutive payments moves the account to a review status.
\"\"\"
question = "What happens if I miss a payment?"
```
""")

code("""repayment_policy = \"\"\"
Repayment Policy (Synthetic Example):
- Repayments are due on the 5th of every month.
- A grace period of 3 days is given before a late fee applies.
- Missing 2 consecutive payments moves the account to a review status.
\"\"\"
question = "What happens if I miss a payment?"

# Your code here (reuse context_chain from Part 8)
""")

md("""**Solution 4**
```python
print(context_chain.invoke({"context": repayment_policy, "question": question}))
```
The answer should now describe the grace period and review status directly from the
policy text, instead of a generic guess.
""")

md("""### Exercise 5 — Reflection (no code)

**Question:** If this were a real bank, what information would you **not** send
directly to an LLM?

**Solution / discussion points:**
- Full customer account numbers, national ID numbers, or passwords.
- Full account balances or transaction histories, unless the application has
  strict access controls and a clear business need.
- Anything that would let the model (or logs of the conversation) leak one
  customer's private data to another customer or a third party.
In practice, only the minimum information needed to answer the question should ever
reach the prompt, and sensitive fields should be masked, summarised, or excluded.
""")

# ============================================================
# PART 12: RECAP
# ============================================================
md("""## 11. Recap

In this notebook you:
- Installed and configured `langchain-google-genai` without hardcoding an API key.
- Made a direct LLM call and interpreted `response.content`.
- Compared vague vs. well-structured prompts and saw the output change.
- Built a reusable `ChatPromptTemplate` with a `{question}` variable.
- Connected a prompt template, an LLM, and an output parser into one LCEL chain.
- Wrapped the chain in a reusable `ask_customer_support()` function and tested it
  on five different questions.
- Compared answering with and without supplied context — the manual version of RAG.
- Saw conceptually how production RAG systems automate the "find relevant
  information" step using embeddings and a vector database.

### Looking Ahead
The next sessions in this curriculum build on exactly this foundation: automating
retrieval with real vector search, and eventually introducing tools and multi-step
agents. Today's `Prompt Template -> LLM -> Output` chain is the seed every one of
those more advanced patterns grows from.
""")

nb['cells'] = cells

path = os.path.join(os.path.dirname(__file__), "07_LLM_Integration_with_LangChain.ipynb")
nbf.write(nb, path)
print("Notebook written to", path, "with", len(cells), "cells (not auto-executed — requires a personal API key; see README.md).")
