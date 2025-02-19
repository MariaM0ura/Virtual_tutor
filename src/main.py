import time
import json
import os
import streamlit as st
from virtual_tutor.virtual_tutor import VirtualTutor

CHAT_HISTORY_FILE = "chat_history.json"

def load_chat_history():
    """Load chat history from a JSON file."""
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, 'r') as f:
            try:
                history = json.load(f)
                return history
            except json.JSONDecodeError:
                return []
    return []

def save_chat_history(chat_history):
    """Save the chat history to a JSON file."""
    with open(CHAT_HISTORY_FILE, 'w') as f:
        json.dump(chat_history, f, indent=4)

def clear_chat_history():
    """Clear the chat history both from session state and disk."""
    st.session_state.messages = []
    save_chat_history([])

def render_content(text, container):
    """
    Check if the given text is wrapped as a simple LaTeX expression.
    If yes, use st.latex to render the formula; otherwise, use st.markdown.
    """
    stripped = text.strip()
    # Check if the text is a pure LaTeX math expression (wrapped in a single pair of $)
    if stripped.startswith("$") and stripped.endswith("$"):
        # Render the inner LaTeX content
        container.latex(stripped.strip("$"))
    else:
        container.markdown(text)

st.set_page_config(initial_sidebar_state="collapsed")

st.title("Tutor Virtual - Chatbot")

if "tutor" not in st.session_state:
    st.session_state.tutor = VirtualTutor()

# Initialize the chat history from file if not already in session_state
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# Sidebar button to clear the history
if st.sidebar.button("Clear Chat History"):
    clear_chat_history()
    st.sidebar.success("History cleared!")

# Display the past messages saved in chat history.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Digite sua questão de matemática..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Save the updated chat history right after appending the user message.
    save_chat_history(st.session_state.messages)
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.spinner("Processando sua pergunta..."):
        response = st.session_state.tutor.handle_query(prompt)
        response_dict = response.model_dump()  

    with st.chat_message("assistant"):
        container = st.container()
        if isinstance(response_dict, dict) and "steps" in response_dict:
            steps = response_dict.get("steps", [])
            if isinstance(steps, dict):
                steps = [steps[key] for key in sorted(steps, key=lambda k: int(k))]
            for i, step in enumerate(steps):
                container.markdown(f"**Passo {i+1}:**")
                container.markdown(f"*Explicação:* {step.get('explanation', '')}")
                output_text = step.get("output", "")
                container.markdown("*Saída:*")
                render_content(output_text, container)
                container.markdown("---")
                time.sleep(0.1) 

        if "final_answer" in response_dict:
            container.markdown("**Resposta Final:**")
            final_ans = response_dict["final_answer"]
            render_content(final_ans, container)
    
    st.session_state.messages.append({"role": "assistant", "content": response_dict.get("final_answer", "")})
    # Save the updated chat history after appending the assistant message.
    save_chat_history(st.session_state.messages)