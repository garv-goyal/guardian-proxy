import streamlit as st
import requests

st.set_page_config(page_title="Guardian AI Firewall", page_icon="🛡️")

st.title("🛡️ Guardian AI Proxy")
st.write("Secure LLM Gateway backed by Google Vertex AI and Datadog.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter a prompt (try a jailbreak!):"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


    with st.spinner("Guardian is analyzing..."):
        try:
            backend_url = "http://127.0.0.1:5000/chat"
            response = requests.post(backend_url, json={"prompt": prompt}, timeout=10)
            
            if response.status_code == 200:
                answer = response.json().get("response")
                st.success("✅ Prompt Allowed")
            elif response.status_code == 403:
                answer = "⛔ SECURITY ALERT: This prompt was flagged and blocked by the Guardian Firewall."
                st.error("🚨 Malicious Intent Detected")
            else:
                answer = "Error: System unavailable."
            
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            st.error(f"Connection Error: {e}")