import streamlit as st
from openai import OpenAI

# 1. Page Configuration
st.set_page_config(page_title="SportsPrompt.pro", page_icon="🏈", layout="centered")

# 2. Strict System Prompt
SYSTEM_PROMPT = """
You are the AI behind SportsPrompt.pro, an elite, highly meticulous sports historian, rulebook expert, and statistician. 
Your prime directive is 100% factual accuracy regarding sports rules, history, and records. 
- NEVER guess. If you do not know a stat or fact, state exactly that.
- ONLY discuss sports. If a user asks about anything unrelated to sports (e.g., coding, politics, weather), politely decline and steer them back to sports.
- Maintain a professional, highly knowledgeable, and engaging tone.
"""

# 3. Initialize API Client
if "OPENAI_API_KEY" not in st.secrets:
    st.error("Please add your OPENAI_API_KEY to Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 4. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Welcome to SportsPrompt.pro. What sports trivia, rule, or historical record can I look up for you?"}
    ]

# 5. Display Chat History (hiding the system prompt)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 6. Chat Input & API Call
if prompt := st.chat_input("Ask a sports question..."):
    # Display user input
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call OpenAI API
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o-mini", # High intelligence, low cost
            messages=st.session_state.messages,
            temperature=0.2, # Low temperature forces factual precision
            stream=True
        )
        response = st.write_stream(stream)
        
    st.session_state.messages.append({"role": "assistant", "content": response})
