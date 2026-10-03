"""Builds Generative_Models_and_Career_Launch_Deploying_Generative_AI_Applications.ipynb.

The notebook is not executed during the build. It calls the Gemini API, which needs a
personal API key that must never be stored in this folder. Run it once, top to bottom,
with your own key before teaching (see ../trainer_guide.md).

The app.py written by the notebook is read from ../app_template/app.py, so the notebook
and the reference app can never drift apart.
"""
import os
import re

import nbformat as nbf

HERE = os.path.dirname(os.path.abspath(__file__))
APP_SOURCE = open(os.path.join(HERE, "..", "app_template", "app.py"), encoding="utf-8").read()

# Reuse the exact knowledge base and prompt from app.py inside the notebook.
BANK_BLOCK = re.search(r"BANK_DOCUMENTS = \{.*?\n\}\n", APP_SOURCE, re.S).group(0).strip()
PROMPT_BLOCK = re.search(r"PROMPT = ChatPromptTemplate.*?\n\]\)\n", APP_SOURCE, re.S).group(0).strip()

nb = nbf.v4.new_notebook()
cells = []


def md(text):
    cells.append(nbf.v4.new_markdown_cell(text.strip("\n")))


def code(text):
    cells.append(nbf.v4.new_code_cell(text.strip("\n")))


# ============================================================
# INTRODUCTION
# ============================================================
md(r"""
# Generative Models & Career Launch
### Topic 9: Deploying Generative AI Applications (hands-on hour)

## Where We Are in the Course

```
Topic 6: Optimization & the ML-to-LLM Bridge   -> how ML systems are designed and tuned
Topic 7: LLM Integration with LangChain        -> prompts, LLM APIs, the first chain
Topic 8: Developing Apps with LangChain        -> RAG, memory, Gradio, testing
Topic 9: Generative Models & Career Launch     -> build, DEPLOY and PRESENT an app   <- today
```

In Topic 8 our microfinance support assistant worked, but **only inside a notebook**.
Nobody else could use it. Today we turn it into a real web application with a public
link, and then into a portfolio project you can show an employer.

## What You Will Build

A **Microfinance Customer Support Assistant** web app:

```
Customer
   |
Web page (Streamlit)              <- what the customer sees
   |
Application logic (Python)        <- our functions
   |
Prompt template + bank context    <- LangChain, retrieval from bank documents
   |
Generative AI model (Gemini)      <- writes the answer
   |
Answer + sources shown on the page
```

## Plan for the Hour

| Time | Part | What you do |
| --- | --- | --- |
| 0-8 min | 1. Setup | Install packages, add your API key safely |
| 8-12 min | 2. First model call | Python -> API -> model -> response |
| 12-20 min | 3. Prompt + context | Build `answer_customer_question(question, context)` |
| 20-32 min | 4. LangChain | Prompt template + retriever + chain: `ask_assistant(question)` |
| 32-42 min | 5. User interface | Write `app.py` with Streamlit and test it |
| 42-50 min | 6. Prepare for deployment | `requirements.txt`, secrets, project folder |
| 50-55 min | 7. Deployment demo | GitHub + Streamlit Community Cloud (trainer demo) |
| 55-60 min | 8. Portfolio | README, CV statement, checklist |

Exercises come after Part 8. Do Exercise 1 in class if you have time; the rest are homework.

## Before You Start
- A free **Google AI Studio API key** (the one from Topics 7 and 8 works).
- For Part 7 (deployment): a free **GitHub** account. You will sign in to Streamlit
  Community Cloud with it.
- All bank names, policies, figures and phone numbers here are **synthetic**. They were
  invented for teaching and describe no real bank.
""")

# ============================================================
# PART 1: SETUP
# ============================================================
md(r"""
## Part 1: Setup (0-8 min)

### Concept
We need three packages:

| Package | Job | Seen before? |
| --- | --- | --- |
| `langchain-core` | Prompt templates, chains, documents, vector store | Topics 7 and 8 |
| `langchain-google-genai` | Connects LangChain to Google's Gemini models | Topics 7 and 8 |
| `streamlit` | Turns a Python script into a web page | **New today** |

In Topic 8 we used **Gradio** for the chat window. Today we use **Streamlit**, because it
can be deployed for free straight from a GitHub repository (more on this in Part 7).
""")

code(r"""
!pip install -qU langchain-core langchain-google-genai streamlit
""")

code(r"""
import os
import re
import time

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore

print("Imports successful.")
""")

md(r"""
### Your API Key

**What is it?** A long secret string that identifies *you* to Google's servers. Every
request our code sends to Gemini carries this key.

**Why do we need it?** The model does not run in Colab. It runs on Google's computers.
The key tells Google who is asking, so it can apply your free-tier limits.

**Why must it stay private?** Treat it like your ATM card and PIN together. Anyone who has
it can send requests in your name and use up your quota (or your money, on a paid plan).

We use the same safe method as Topics 7 and 8: **Colab Secrets** (key icon in the left
sidebar, secret name `GOOGLE_API_KEY`, notebook access switched on). If no secret is found,
you will be asked to type the key. It is never printed or saved in the notebook.
""")

code(r"""
api_key = None

try:
    from google.colab import userdata
    api_key = userdata.get("GOOGLE_API_KEY")
except Exception:
    pass

if not api_key:
    import getpass
    api_key = getpass.getpass("Enter your Google AI Studio API key: ")

os.environ["GOOGLE_API_KEY"] = api_key   # an environment variable: the same idea we use when deploying
print("API key configured.")
""")

md(r"""
> **Remember for later:** we stored the key in an **environment variable**
> (`os.environ`). Our deployed app will read the key in exactly the same way. Only the
> place where we *set* it changes (Colab Secrets now, Streamlit Secrets in Part 7).
""")

# ============================================================
# PART 2: FIRST MODEL CALL
# ============================================================
md(r"""
## Part 2: Call the Generative Model (8-12 min)

### Concept
```
Python code  --->  API (internet)  --->  Gemini model (Google's servers)  --->  response
```
A predictive model from Topic 6 returned a **number or a label**. A generative model
returns **new text** that did not exist before. Let's ask it to write a support reply.
""")

code(r"""
llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0.2)

start = time.time()
response = llm.invoke(
    "You are a customer support assistant for a microfinance bank in Nigeria. "
    "A customer asks: 'How do I open a savings account?' Reply in two short sentences."
)
seconds = time.time() - start

print(response.text)
print()
print(f"Time taken: {seconds:.1f} seconds")
print("Tokens used:", response.usage_metadata)
""")

md(r"""
### Interpretation
- **`response.text`** is the generated answer. (Newer Gemini models return a list of
  content blocks, so we read `.text` rather than `.content`.)
- **Time taken** is the *latency*. A user of our web app will wait this long for every answer.
- **Tokens used** drives *cost*. On a paid plan you pay per input and output token. On the
  free tier, tokens count towards your limits.

**Trainer Question:** The answer sounds confident. Does the model know *our* bank's
minimum deposit? Where would it get that information?

> Expected answer: No. It is guessing from general knowledge. Nothing about our bank was
> in the prompt. We fix that in Part 3 by giving it **context**.
""")

# ============================================================
# PART 3: PROMPT + CONTEXT FUNCTION
# ============================================================
md(r"""
## Part 3: Build the Application Logic (12-20 min)

### Concept
A good support prompt has three parts:

```
Instructions  (who you are, rules)  +  Context  (the bank's facts)  +  Question
```

We wrap this in a **reusable function**. A function is the bridge between a notebook and
an application: a web page, a WhatsApp bot or a test script can all call the same function.

First, the bank's knowledge. These are the same six synthetic policies from Topic 8.
""")

code(BANK_BLOCK + r"""

print("Policies loaded:", list(BANK_DOCUMENTS))
""")

code(r"""
def answer_customer_question(question, context):
    '''Build a prompt from instructions + context + question, call the model, return the text.'''
    prompt = (
        "You are a customer support assistant for a microfinance bank.\n"
        "Answer using ONLY the bank information below. If the answer is not there, "
        "say: I don't have that information.\n"
        "Keep the answer under 80 words, in simple English.\n\n"
        f"Bank information:\n{context}\n\n"
        f"Customer question: {question}"
    )
    response = llm.invoke(prompt)
    return response.text
""")

code(r"""
question = "What happens if I pay my loan 2 days late?"

print("WITHOUT context:")
print(answer_customer_question(question, context="(no information provided)"))
print("-" * 60)
print("WITH context:")
print(answer_customer_question(question, context=BANK_DOCUMENTS["Repayment Policy"]))
""")

md(r"""
### Interpretation
- Without context, the model has no facts, so it should say it does not have the
  information (because our prompt told it to).
- With the Repayment Policy as context, it can mention the **3-day grace period**: the
  answer is now **grounded** in the bank's own document.

**Why a function?** We wrote the prompt once. Now any question, any context, any caller
(test script, web page) uses the same logic. If the bank changes a rule, we change it in
one place.

**Problem:** we chose the context *by hand*. A real customer could ask about anything.
In Topic 8 we solved this with **retrieval**. Let's bring that back with LangChain.
""")

# ============================================================
# PART 4: LANGCHAIN
# ============================================================
md(r"""
## Part 4: Use LangChain (20-32 min)

### Concept
Same idea as Part 3, organised with the LangChain pieces from Topics 7 and 8:

```
Question -> Retriever (finds the right policies) -> Context
         -> Prompt Template -> LLM -> Output Parser -> Answer + Sources
```

### 4.1 The Prompt Template and the Chain
""")

code(r"""
REFUSAL = "I don't have that information."

""" + PROMPT_BLOCK + r"""

chain = PROMPT | llm | StrOutputParser()
print("Chain ready:", chain)
""")

md(r"""
The `system` message holds the rules and the context. The `human` message holds the
question. Rule 2 gives an **exact** refusal sentence, so our code can detect it.

### 4.2 The Retriever (from Topic 8)
We embed the six policies and keep them in an in-memory vector store. Each policy is
short, so we do not split it into chunks this time. `k=2` returns the two closest policies.
""")

code(r"""
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

docs = [Document(page_content=text, metadata={"source": title})
        for title, text in BANK_DOCUMENTS.items()]

vector_store = InMemoryVectorStore(embeddings)
vector_store.add_documents(docs)
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

for d in retriever.invoke("Someone stole my card"):
    print("Found:", d.metadata["source"])
""")

md(r"""
### 4.3 One Function for the Whole Assistant
`ask_assistant` is the heart of our application. It also hides account numbers and BVNs
(the `mask_sensitive` guardrail from Topic 8) before anything is sent to the model.
""")

code(r"""
def mask_sensitive(text):
    '''Hide 10-digit account numbers and 11-digit BVNs.'''
    return re.sub(r"\b\d{10,11}\b", "[HIDDEN NUMBER]", text)


def format_docs(found_docs):
    return "\n\n".join(f"[{d.metadata['source']}]\n{d.page_content}" for d in found_docs)


def ask_assistant(question):
    '''Question in, (answer, sources) out.'''
    question = mask_sensitive(question)
    found = retriever.invoke(question)
    answer = chain.invoke({"context": format_docs(found), "question": question})
    if REFUSAL.lower() in answer.lower():
        return answer, []
    return answer, sorted({d.metadata["source"] for d in found})
""")

code(r"""
test_questions = [
    "What documents do I need for a business loan?",
    "What time do you open on Saturday?",
    "Do you offer mortgages?",                               # not in our documents
    "My account number is 0123456789. What is my balance?",  # sensitive data
]

for q in test_questions:
    answer, sources = ask_assistant(q)
    print("Q:", q)
    print("A:", answer)
    print("Sources:", ", ".join(sources) if sources else "none")
    print("-" * 60)
    time.sleep(2)   # stay inside the free tier's requests-per-minute limit
""")

md(r"""
### Interpretation
- The first two answers should quote our synthetic policies and list their sources.
- "Mortgages" should get the refusal sentence: the bank does not offer them, and the
  assistant must not invent one. This is how we limit **hallucination**.
- The account number never reaches the model: it was replaced with `[HIDDEN NUMBER]`.

**Trainer Question:** Our assistant works. Could a customer in Kano use it right now?
What is missing?

> Expected answer: No. It only runs inside this notebook, on our Colab session, and needs
> our Python code and our key. It needs a web page and a public address. That is Parts 5 to 7.
""")

# ============================================================
# PART 5: USER INTERFACE
# ============================================================
md(r"""
## Part 5: A Simple User Interface with Streamlit (32-42 min)

### Concept
**Streamlit** turns a normal Python script into a web page. Each `st.` command adds
something to the page:

| Code | What appears on the page |
| --- | --- |
| `st.title("...")` | A big title |
| `st.text_input("Your question")` | A text box |
| `st.form_submit_button("Ask")` | A submit button |
| `st.markdown(answer)` | The response area |

One idea to remember: **Streamlit runs the whole script from top to bottom every time
the user clicks something.** So anything slow (creating the model, embedding the
documents) goes inside a function marked `@st.cache_resource`. It then runs **once** and
is reused for every visitor, which saves time *and* API calls.

### Why Streamlit and not Gradio?
Both are good. We used Gradio in Topic 8. For **free** hosting in 2026, Streamlit has the
simplest route: **Streamlit Community Cloud** deploys straight from GitHub at no cost.
Hugging Face Spaces, the usual home of Gradio apps, now requires a paid plan to create
new Gradio Spaces (free accounts can host a small number on ZeroGPU only).

### 5.1 Write `app.py`
`%%writefile` saves the cell as a file instead of running it. This file **is** our
application. Read it top to bottom: it is the same code as Parts 3 and 4, organised into
four sections.
""")

code("%%writefile app.py\n" + APP_SOURCE.rstrip("\n"))

md(r"""
### What Changed from the Notebook?

| Section in `app.py` | Where it came from |
| --- | --- |
| 1. Settings | Part 2 (model names) |
| 2. Bank knowledge + `PROMPT` | Parts 3 and 4.1 |
| 3. Application logic | Part 4: `mask_sensitive`, `format_docs`, `ask_assistant`. The model, retriever and chain are built inside `load_assistant`, which runs once thanks to `@st.cache_resource`, so `ask_assistant` receives the retriever and chain as inputs. |
| 4. User interface | **New**: title, text box, Ask button, answer area, error message |

Three things a notebook never needed, but an app does:
- **`get_api_key()`** reads the key from an environment variable or Streamlit secrets. No key
  is written in the file.
- **`try / except`** shows a polite message if the API fails, instead of a crash.
- **`max_chars=300`** stops very long questions, which keeps costs under control.

### 5.2 Test the App Without a Browser
Streamlit includes a testing tool, `AppTest`. It runs `app.py`, types a question, clicks
**Ask**, and lets us read what appeared on the page. The app finds our key in the
`GOOGLE_API_KEY` environment variable we set in Part 1.
""")

code(r"""
from streamlit.testing.v1 import AppTest

at = AppTest.from_file(os.path.abspath("app.py"), default_timeout=60)   # AppTest needs the full path
at.run()
print("Page title:", at.title[0].value)

at.text_input[0].input("What do I need to open a savings account?")
at.button[0].click().run()

print("Errors on page:", [e.value for e in at.error])
print("Answer:", at.main.markdown[-1].value)   # the last text block in the main page is the answer
print("Sources:", [c.value for c in at.caption if c.value.startswith("Sources")])
""")

md(r"""
### Interpretation
If you see the title, an answer about the 1,000 NGN minimum deposit, and a "Sources"
line, the **whole application works**: interface, logic, prompt, retrieval and model.

### 5.3 (Optional) See the Page in Your Browser
This starts the app on Colab's computer (port 8501) and opens it in a new browser tab.
Only you can see this tab: it is still **not** deployed. If it does not open, skip it.
The test above already proved the app works.
""")

code(r"""
import subprocess

server = subprocess.Popen(
    ["streamlit", "run", "app.py", "--server.port", "8501", "--server.headless", "true"]
)
time.sleep(8)   # give Streamlit a few seconds to start

from google.colab import output
output.serve_kernel_port_as_window(8501)
""")

code(r"""
# Run this when you have finished looking at the page, to stop the local app
server.terminate()
""")

# ============================================================
# PART 6: PREPARE FOR DEPLOYMENT
# ============================================================
md(r"""
## Part 6: Prepare for Deployment (42-50 min)

### Concept: Notebook -> Application

| | In this notebook | In the deployed app |
| --- | --- | --- |
| Code | Many cells | One file: `app.py` |
| Packages | `!pip install` | `requirements.txt` |
| API key | Colab Secrets | Streamlit Cloud **Secrets** |
| How it runs | Shift + Enter | Streamlit Cloud runs `app.py` on its server |
| Who can use it | Only you | Anyone with the link |
| Where the code lives | Your Colab session | A **GitHub repository** |

### 6.1 `requirements.txt`
The server that hosts our app starts empty. `requirements.txt` lists the packages it must
install. We pin the **exact versions** we just tested, so the server installs the same ones.
""")

code(r"""
from importlib.metadata import version

packages = ["streamlit", "langchain-core", "langchain-google-genai"]
requirements = "\n".join(f"{p}=={version(p)}" for p in packages) + "\n"

with open("requirements.txt", "w") as f:
    f.write(requirements)

print(requirements)
""")

md(r"""
### 6.2 Keep Secrets Out of the Code
Our `app.py` contains **no key**. When deployed, Streamlit Community Cloud will hold the
key for us. You will paste it into the app's **Secrets** box in TOML format:

```toml
GOOGLE_API_KEY = "paste-your-key-here"
```

Streamlit makes top-level secrets available as environment variables **and** through
`st.secrets`, so `get_api_key()` finds it either way.

If you ever run the app on your own laptop, you can keep the key in a file called
`.streamlit/secrets.toml`. That file must **never** go to GitHub, so we also create a
`.gitignore` file, which tells Git which files to leave out.
""")

code(r"""
gitignore = '''# Never upload secrets or local clutter
.streamlit/secrets.toml
.env
__pycache__/
'''
with open(".gitignore", "w") as f:
    f.write(gitignore)

print(gitignore)
""")

md(r"""
### 6.3 Package the Project Folder
""")

code(r"""
import shutil

project = "microfinance-support-assistant"
os.makedirs(project, exist_ok=True)
for file_name in ["app.py", "requirements.txt", ".gitignore"]:
    shutil.copy(file_name, project)

print("Project folder contents:")
for file_name in sorted(os.listdir(project)):
    print("  ", file_name)

# Final safety check: the key must not appear in any file we are about to share
for file_name in os.listdir(project):
    with open(os.path.join(project, file_name)) as f:
        assert api_key not in f.read(), f"STOP: your API key is inside {file_name}!"
print("Safety check passed: no API key in the project files.")
""")

code(r"""
shutil.make_archive(project, "zip", project)

try:
    from google.colab import files
    files.download(project + ".zip")
except Exception:
    print("Download", project + ".zip", "from the Files panel on the left.")
""")

md(r"""
Unzip the download on your computer. You now have the three files a deployment needs.

> **Hidden file note:** `.gitignore` starts with a dot, so your computer may hide it.
> That is fine for today: our project has no secrets file to protect. It matters as soon
> as you work with Git on your own laptop.
""")

# ============================================================
# PART 7: DEPLOYMENT DEMONSTRATION
# ============================================================
md(r"""
## Part 7: Deploy to Streamlit Community Cloud (50-55 min, trainer demo)

Your trainer will do this live. Follow along now if time allows, or repeat it after
class: it takes about 10 minutes the first time.

### Development -> Deployment -> Monitoring

| Stage | Meaning | Restaurant analogy |
| --- | --- | --- |
| **Development** | "I'm building and testing the application." | Cooking and tasting in your own kitchen |
| **Deployment** | "I'm making the application available for other people to use." | Opening the restaurant to customers |
| **Monitoring** | "I'm checking whether it keeps working properly." | Checking food quality and reading customer complaints |

### Step A: Put the Code on GitHub
1. Sign in at https://github.com and click **+** (top right) then **New repository**.
2. Name it `microfinance-support-assistant`, choose **Public**, then **Create repository**.
3. On the empty repository page, click **uploading an existing file**.
4. Drag in `app.py` and `requirements.txt` from the unzipped folder.
5. Click **Commit changes**.

### Step B: Deploy the App
1. Go to https://share.streamlit.io and sign in with **GitHub** (allow Streamlit to see
   your repositories when asked).
2. Click **Create app** (top right), then **Yup, I have an app**.
3. Fill in:
   - **Repository:** `your-username/microfinance-support-assistant`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** optional, choose a short name
4. Click **Advanced settings**. Keep the default Python version. In **Secrets**, paste:
   ```toml
   GOOGLE_API_KEY = "paste-your-key-here"
   ```
   Click **Save**.
5. Click **Deploy**. The first build usually takes a few minutes while packages install.

### Step C: Test It Like a Customer
- Open the `https://....streamlit.app` link in a private/incognito window or on your phone.
- Ask a question the app should answer, and one it should refuse (for example, mortgages).
- Share the link with a classmate.

### Step D: Update and Monitor
- **Update:** edit a file on GitHub and commit. Streamlit Cloud picks up the change and
  updates the app automatically.
- **Monitor:** open your app and click **Manage app** (bottom right) to see the logs. The
  line `Model call failed: ...` from our `try / except` appears there.
- **Sleep:** free apps with no visitors for 12 hours go to sleep. Anyone who opens the link
  can wake it up with one click; it takes a little while to start again.

### If Something Goes Wrong

| What you see | Likely cause | Fix |
| --- | --- | --- |
| `ModuleNotFoundError` in the logs | Package missing from `requirements.txt` | Add it, commit, wait for the rebuild |
| "No API key found" on the page | Secret missing or misnamed | **Settings > Secrets**: it must be exactly `GOOGLE_API_KEY` |
| "Assistant is not available right now" | Wrong key, or free-tier limit reached | Check the key in AI Studio; wait a minute and retry |
| App takes a long time to open | It was asleep, or is still building | Wait; check the logs under **Manage app** |
| GitHub blocks your push with a secret warning | A key was found in your files (push protection) | Remove the key from the file. Use Secrets instead |

### Where Else Could This Run?
- **Hugging Face Spaces** hosts Gradio and Docker apps. Free personal accounts (verified
  email, older than 30 days) can host up to 2 ZeroGPU Spaces; other Gradio Spaces need a
  paid plan.
- **Cloud platforms** (Google Cloud Run, Azure, AWS) give more control and scale, but need
  a billing account and more setup. That is a future topic.
""")

# ============================================================
# PART 8: PORTFOLIO
# ============================================================
md(r"""
## Part 8: Turn It into a Portfolio Project (55-60 min)

### Concept
An employer will spend about a minute on your repository. The **README** is what they
read first. A working app with no explanation looks like a tutorial copy. A clear README
shows that you understand the **problem**, the **design** and the **limits**.

The cell below writes a README for your repository. Replace the `[...]` parts with your
own details, then upload it to GitHub (**Add file > Upload files**). GitHub draws the
architecture diagram from the `mermaid` block automatically.
""")

code(r'''
readme = """# Microfinance Customer Support Assistant

A Generative AI web app that answers customer questions about a (synthetic) microfinance
bank's loans, repayments, savings and security policies.

**Live demo:** [paste your .streamlit.app link]

## Problem
Customer support staff answer the same policy questions every day: loan documents,
repayment dates, late fees, opening hours. Customers wait in queues for simple answers.

## Solution
An assistant that finds the relevant bank policy and writes a short, plain-English answer,
showing which policy it used. It refuses questions the policies do not cover.

## Features
- Answers only from the bank's policy documents and shows its sources
- Says "I don't have that information" instead of guessing
- Hides account numbers and BVNs before anything is sent to the model
- Simple web interface; API key kept in platform secrets, not in code

## Architecture
```mermaid
flowchart TD
    A[Customer] --> B[Streamlit web page]
    B --> C[App logic: ask_assistant]
    C --> D[Retriever: finds 2 closest policies]
    D --> E[LangChain prompt template + context]
    E --> F[Gemini model]
    F --> G[Answer + sources shown on page]
```

## Technologies
Python, LangChain (`langchain-core`, `langchain-google-genai`), Google Gemini
(`gemini-flash-latest`, `gemini-embedding-001`), Streamlit, Streamlit Community Cloud, GitHub.

## How It Works
1. The six policy documents are turned into embeddings and stored in memory (once, at startup).
2. A customer's question is masked, then used to retrieve the two closest policies.
3. A prompt template combines rules, the retrieved policies and the question.
4. Gemini writes the answer; the app shows it with its sources.

## Testing
[Describe the questions you tested: some it should answer, some it should refuse, and the results.]

## Limitations
- Uses synthetic policies; not connected to real accounts or real customer data.
- Can still produce wrong or incomplete answers; important decisions need a human.
- The free tier limits how many questions can be answered per minute.
- Masking only catches 10 and 11 digit numbers.

## Future Improvements
[e.g. chat memory, more documents, a feedback button, automated tests, a WhatsApp channel]

## Run It Yourself
1. `pip install -r requirements.txt`
2. Set the `GOOGLE_API_KEY` environment variable (never commit it)
3. `streamlit run app.py`
"""

with open(os.path.join(project, "README.md"), "w") as f:
    f.write(readme)
print("README.md written to", project)
''')

md(r"""
### Say What You Built, Not What You "Know"

| Weak CV statement | Stronger project statement |
| --- | --- |
| "Worked with AI and LangChain." | "Built and deployed a Generative AI customer-support assistant that combines an LLM, prompt templates, retrieval of policy documents and a Streamlit web interface to answer customer questions." |
| "I know Generative AI." | "I built and deployed a Generative AI customer-support application using Python, LangChain, an LLM API, retrieval-based context and a web interface." |

Describe what you **built** and **how**. Do **not** claim results you did not measure
(for example, "reduced support calls by 40%").

### Your 60-Second Interview Explanation
**Problem -> Approach -> Technology -> Architecture -> Result -> Limitations -> Improvement**

> "Microfinance support teams answer the same policy questions every day. I built an
> assistant that answers them from the bank's own policy documents. It retrieves the two
> most relevant policies, puts them into a LangChain prompt template, and asks a Gemini
> model to answer in plain English, showing its sources. I deployed it with Streamlit
> Community Cloud, with the API key stored as a platform secret. In my tests it answered
> policy questions correctly and refused questions the documents don't cover, like
> mortgages. Its limits: it uses synthetic data and can still make mistakes, so a real bank
> would need human review. Next, I'd add a test suite and a feedback button."

### Portfolio Checklist
**Technical:** working app · GitHub repository · clean code · `requirements.txt` ·
secrets kept out of code · README · architecture diagram · deployed demo

**Data/AI:** problem defined · model named · prompt documented · context/RAG explained ·
testing described · limitations listed

**Career:** project on your CV · LinkedIn project post · portfolio page · short project
description · interview explanation practised

A full template is in `portfolio_template.md` in the course folder.
""")

# ============================================================
# EXERCISES
# ============================================================
md(r"""
## Exercises

Try each one before opening the solution below it. Exercises 1 and 2 use the notebook
functions; the same changes can then be copied into `app.py`.

### Exercise 1: A More Concise Assistant
Customers on mobile phones want short answers. Change the rules in `PROMPT` so answers are
**one or two sentences, under 30 words**. Rebuild `chain` and compare the answer length for
`"What documents do I need for a business loan?"`.
""")

code(r"""
# Exercise 1: your code here
""")

md(r"""
**Solution 1**
```python
concise_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are the customer support assistant for a microfinance bank.\n"
     "Rules:\n"
     "1. Answer using ONLY the bank information below.\n"
     "2. If the answer is not in the bank information, reply exactly: " + REFUSAL + "\n"
     "3. Never ask for, or repeat, account numbers, BVNs, PINs or passwords.\n"
     "4. Answer in one or two sentences, under 30 words.\n\n"
     "Bank information:\n{context}"),
    ("human", "{question}"),
])

q = "What documents do I need for a business loan?"
context = format_docs(retriever.invoke(q))

long_answer = chain.invoke({"context": context, "question": q})
short_answer = (concise_prompt | llm | StrOutputParser()).invoke({"context": context, "question": q})

print(len(long_answer.split()), "words:", long_answer)
print(len(short_answer.split()), "words:", short_answer)
```
Only the instruction changed. The model, retriever and app stayed the same. Shorter answers
also mean fewer output tokens, so lower cost and latency.
""")

md(r"""
### Exercise 2: Add Another Piece of Context
The bank has launched a **School Fees Loan** (synthetic):

```
School Fees Loan: for parents and guardians paying school fees. Maximum 300,000 NGN.
Interest is 2% per month. Repaid over 3 to 6 months. Requires the school's fee invoice
and a valid government-issued ID.
```
Add it to `BANK_DOCUMENTS` and to the vector store, then ask
`"Can I borrow money for my child's school fees?"`.
""")

code(r"""
# Exercise 2: your code here
""")

md(r"""
**Solution 2**
```python
school_fees = ("School Fees Loan: for parents and guardians paying school fees. Maximum "
               "300,000 NGN. Interest is 2% per month. Repaid over 3 to 6 months. Requires "
               "the school's fee invoice and a valid government-issued ID.")

BANK_DOCUMENTS["School Fees Loan"] = school_fees
vector_store.add_documents([Document(page_content=school_fees,
                                     metadata={"source": "School Fees Loan"})])

answer, sources = ask_assistant("Can I borrow money for my child's school fees?")
print(answer)
print("Sources:", sources)
```
Before the change, this question should get the refusal sentence. After it, the answer
cites the School Fees Loan. To update the **deployed** app, add the same entry to
`BANK_DOCUMENTS` in `app.py` on GitHub and commit.
""")

md(r"""
### Exercise 3: Return a Structured Response
The bank's system wants each reply as fields, not just text: the `answer`, a `category`
(`loans`, `repayments`, `savings`, `security`, `branch` or `other`) and `needs_human`
(True for fraud, a stolen card, or a customer who cannot pay). Use a Pydantic class and
`llm.with_structured_output(...)` (from Topic 8).
""")

code(r"""
# Exercise 3: your code here
""")

md(r"""
**Solution 3**
```python
from typing import Literal
from pydantic import BaseModel, Field

class SupportReply(BaseModel):
    answer: str = Field(description="Short answer for the customer, using only the bank information")
    category: Literal["loans", "repayments", "savings", "security", "branch", "other"]
    needs_human: bool = Field(description="True for fraud, a stolen card, or a customer who cannot pay")

structured_chain = PROMPT | llm.with_structured_output(SupportReply)

q = "I lost my job and can't pay this month's instalment."
reply = structured_chain.invoke({"context": format_docs(retriever.invoke(q)), "question": q})
print(reply.category, "| needs human:", reply.needs_human)
print(reply.answer)
```
Now the app can act on the fields, for example `if reply.needs_human:` show the helpline
and alert a loan officer. Structured output fixes the **format**; it does not make the
answer more accurate, so we still test it.
""")

md(r"""
### Exercise 4: Improve the App for Another Question
Ask `ask_assistant("I think someone stole my card. What do I do?")`. A worried customer
needs the helpline number **first**. Add a rule to the prompt so that any lost card, stolen
card or fraud question starts with the 24-hour helpline number. Test it with two different
wordings.
""")

code(r"""
# Exercise 4: your code here
""")

md(r"""
**Solution 4**
```python
safety_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are the customer support assistant for a microfinance bank.\n"
     "Rules:\n"
     "1. Answer using ONLY the bank information below.\n"
     "2. If the answer is not in the bank information, reply exactly: " + REFUSAL + "\n"
     "3. Never ask for, or repeat, account numbers, BVNs, PINs or passwords.\n"
     "4. Keep answers under 80 words, in simple English.\n"
     "5. If the customer mentions a lost or stolen card, or fraud, start your answer with: "
     "Call our 24-hour helpline now on 0700-000-0000.\n\n"
     "Bank information:\n{context}"),
    ("human", "{question}"),
])
chain = safety_prompt | llm | StrOutputParser()   # ask_assistant uses the new chain

for q in ["I think someone stole my card. What do I do?",
          "There are withdrawals on my account that I didn't make."]:
    answer, sources = ask_assistant(q)
    print(q, "\n ->", answer, "\n")
```
Test with more than one wording: customers rarely use the exact words you expect.
""")

md(r"""
### Exercise 5: Write Your README Description
Write a 3 to 4 sentence "About this project" paragraph for your GitHub repository. It must
say: the problem, what the app does, the main technologies, and one limitation. Do not
claim results you have not measured.

**Sample answer**
> Microfinance customers often wait in queues to ask simple policy questions. This project
> is a Generative AI support assistant that answers those questions from the bank's own
> policy documents, shows which policy it used, and refuses questions it cannot answer.
> It is built with Python, LangChain and Google's Gemini model, and deployed as a Streamlit
> web app. It uses synthetic policies and can still make mistakes, so it is a prototype,
> not a replacement for trained staff.
""")

# ============================================================
# RECAP
# ============================================================
md(r"""
## Recap

Today you moved from **experiment -> application -> deployment -> portfolio**:

1. Called a generative model through an API and measured its **latency** and **tokens**.
2. Wrapped instructions + context + question into a reusable **function**.
3. Rebuilt it with **LangChain**: a prompt template, a retriever and a chain.
4. Turned it into a **Streamlit** web app (`app.py`) and tested it with `AppTest`.
5. Prepared it for deployment: `requirements.txt`, **secrets** instead of hardcoded keys.
6. Saw how to **deploy** it from GitHub to Streamlit Community Cloud.
7. Wrote a **README** and a CV statement that describe what you actually built.

### Your Next Step
Finish the deployment, put the link in your README, and add the project to your CV and
LinkedIn this week. Then build a second project for a different problem (for example, a
clinic appointment FAQ assistant) using the same pattern.
""")

nb["cells"] = cells
nb["metadata"]["colab"] = {"provenance": []}
nb["metadata"]["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}

path = os.path.join(HERE, "Generative_Models_and_Career_Launch_Deploying_Generative_AI_Applications.ipynb")
nbf.write(nb, path)
print("Notebook written to", path, "with", len(cells), "cells.")
