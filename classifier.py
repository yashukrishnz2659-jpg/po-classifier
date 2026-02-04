import streamlit as st
from prompts import SYSTEM_PROMPT

MODEL = "openai/gpt-oss-120b"


@st.cache_resource
def get_groq_client():
    try:
        from groq import Groq
    except ImportError:
        st.error("Groq package not installed. Add `groq` to requirements.txt")
        st.stop()

    return Groq(api_key=st.secrets["GROQ_API_KEY"])


def classify_po(po_description: str, supplier: str = "Not provided"):
    client = get_groq_client()

    user_prompt = f"""
PO Description:
{po_description}

Supplier:
{supplier}
"""

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.choices[0].message.content
