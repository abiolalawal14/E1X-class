"""Microfinance Customer Support Assistant (teaching demo).

A small Generative AI application:
    Customer -> Streamlit page -> app logic -> prompt + bank context (LangChain)
             -> Gemini model -> answer shown on the page

All bank information below is synthetic. It describes no real bank.
Run locally with:  streamlit run app.py
"""
import os
import re

import streamlit as st
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

# ---------------------------------------------------------------------------
# 1. Settings
# ---------------------------------------------------------------------------
CHAT_MODEL = "gemini-flash-latest"         # Google alias for the current Flash model
EMBEDDING_MODEL = "gemini-embedding-001"
REFUSAL = "I don't have that information."
MAX_QUESTION_LENGTH = 300                  # keeps prompts (and costs) small

# ---------------------------------------------------------------------------
# 2. The bank's knowledge (synthetic, same policies as Topic 8)
# ---------------------------------------------------------------------------
BANK_DOCUMENTS = {
    "Business Loan Policy": (
        "Business loans are for customers who own a small business. "
        "The business must be registered and active for at least 6 months. "
        "Documents needed: 3 months of bank statements, a valid government-issued ID "
        "and proof of business address such as a utility bill. "
        "First-time business borrowers can borrow up to 500,000 NGN. "
        "Returning borrowers who repaid on time can apply for up to 1,500,000 NGN. "
        "Interest is 2.5% per month on the original loan amount. "
        "Loans are repaid over 6 to 12 months. A decision is usually given within 3 working days."
    ),
    "Personal Loan Policy": (
        "Personal loans are for salary earners employed for at least 6 months. "
        "Applicants provide their last 3 payslips and a valid government-issued ID. "
        "The maximum personal loan is 200,000 NGN. Interest is 3% per month. "
        "Personal loans are repaid over 3 to 9 months."
    ),
    "Repayment Policy": (
        "Repayments are due on the 5th of every month, by bank transfer, at any branch "
        "or in the mobile app. A grace period of 3 days is given before a late fee applies. "
        "The late fee is 2% of the missed instalment. Customers who expect to miss a "
        "payment should contact the bank before the due date. Early repayment is allowed "
        "at any time with no extra charge."
    ),
    "Savings Account": (
        "The Everyday Savings Account can be opened with 1,000 NGN. It earns 4% interest "
        "per year. Customers get 4 free withdrawals each month; each extra withdrawal "
        "costs 50 NGN. To open it, bring a valid government-issued ID and a passport photograph."
    ),
    "Account Security": (
        "The bank will never ask for your PIN, password or one-time code by phone, SMS, "
        "email or chat. If your card is lost or stolen, call the 24-hour helpline on "
        "0700-000-0000 or block the card in the mobile app."
    ),
    "Branch Opening Hours": (
        "Branches open Monday to Friday, 8:00 am to 4:00 pm, and Saturday, 9:00 am to "
        "1:00 pm. Branches are closed on Sundays and public holidays. The mobile app and "
        "the 24-hour helpline are available at all times."
    ),
}

PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are the customer support assistant for a microfinance bank.\n"
     "Rules:\n"
     "1. Answer using ONLY the bank information below.\n"
     "2. If the answer is not in the bank information, reply exactly: " + REFUSAL + "\n"
     "3. Never ask for, or repeat, account numbers, BVNs, PINs or passwords.\n"
     "4. Keep answers under 80 words, in simple English.\n\n"
     "Bank information:\n{context}"),
    ("human", "{question}"),
])


# ---------------------------------------------------------------------------
# 3. Application logic (plain Python functions)
# ---------------------------------------------------------------------------
def get_api_key():
    """Read the key from an environment variable or Streamlit secrets. Never hardcode it."""
    key = os.environ.get("GOOGLE_API_KEY")
    if not key:
        try:
            key = st.secrets["GOOGLE_API_KEY"]
        except Exception:
            key = None
    return key


def mask_sensitive(text):
    """Hide 10-digit account numbers and 11-digit BVNs before text leaves the app."""
    return re.sub(r"\b\d{10,11}\b", "[HIDDEN NUMBER]", text)


def format_docs(docs):
    return "\n\n".join(f"[{d.metadata['source']}]\n{d.page_content}" for d in docs)


@st.cache_resource(show_spinner="Preparing the assistant...")
def load_assistant(api_key):
    """Build the model, the retriever and the chain ONCE, then reuse them for every visitor."""
    llm = ChatGoogleGenerativeAI(model=CHAT_MODEL, temperature=0.2, google_api_key=api_key)
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL, google_api_key=api_key)

    docs = [Document(page_content=text, metadata={"source": title})
            for title, text in BANK_DOCUMENTS.items()]
    vector_store = InMemoryVectorStore(embeddings)
    vector_store.add_documents(docs)
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})

    chain = PROMPT | llm | StrOutputParser()
    return retriever, chain


def ask_assistant(question, retriever, chain):
    """Question in, (answer, sources) out. Same as the notebook version, but the
    retriever and chain are passed in because load_assistant() builds them once."""
    question = mask_sensitive(question)
    found = retriever.invoke(question)
    answer = chain.invoke({"context": format_docs(found), "question": question})
    if REFUSAL.lower() in answer.lower():
        return answer, []
    return answer, sorted({d.metadata["source"] for d in found})


# ---------------------------------------------------------------------------
# 4. User interface (Streamlit)
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Microfinance Support Assistant", page_icon="💬")
st.title("Microfinance Customer Support Assistant")
st.caption("Teaching demo with synthetic bank information. "
           "Do not enter real account numbers or personal details.")

with st.sidebar:
    st.header("About")
    st.write("Answers come from the bank's (synthetic) policy documents, "
             "using LangChain and a Gemini model.")
    st.write("Try: *What documents do I need for a business loan?*")
    st.write("AI answers can be wrong. Confirm important details with a branch.")

api_key = get_api_key()
if not api_key:
    st.error("No API key found. Add GOOGLE_API_KEY to your environment or Streamlit secrets.")
    st.stop()

retriever, chain = load_assistant(api_key)

with st.form("question_form"):
    question = st.text_input("Your question", max_chars=MAX_QUESTION_LENGTH,
                             placeholder="e.g. What happens if I pay 2 days late?")
    submitted = st.form_submit_button("Ask")

if submitted:
    if not question.strip():
        st.warning("Please type a question first.")
    else:
        with st.spinner("Thinking..."):
            try:
                answer, sources = ask_assistant(question, retriever, chain)
            except Exception as error:
                answer, sources = None, []
                st.error("Sorry, the assistant is not available right now. Please try again "
                         "in a minute.")
                print("Model call failed:", repr(error))   # visible in the app logs, not to users
        if answer:
            st.subheader("Answer")
            st.markdown(answer)
            if sources:
                st.caption("Sources: " + ", ".join(sources))
