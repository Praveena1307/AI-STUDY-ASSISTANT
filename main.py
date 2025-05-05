import streamlit as st
import time
from agent import run_agent
from dotenv import load_dotenv
from tools import get_tool_names

def main():
    load_dotenv()
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    st.set_page_config(
        page_title="AI Assistant at Your Service",
        page_icon="🤖",
        layout="wide"
    )
    
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.title("🤖 AI Assistant at Your Service")
        st.markdown("Your personalized study and research companion")
        
        with st.expander("🛠️ Available Tools", expanded=False):
            tools = get_tool_names()
            for tool in tools:
                st.markdown(f"- **{tool}**")
    
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                if "tools_used" in message and message["tools_used"]:
                    with st.expander("🧰 Tools Used"):
                        for tool in message["tools_used"]:
                            st.info(f"**{tool}**")
    
    query = st.chat_input("Ask me anything...")
    
    if query:
        if query.lower() in {"exit", "quit", "bye"}:
            with st.chat_message("user"):
                st.write(query)
            
            with st.chat_message("assistant"):
                st.write("👋 Goodbye! Feel free to return whenever you need assistance.")
                
            st.session_state.chat_history.append({"role": "user", "content": query})
            st.session_state.chat_history.append({"role": "assistant", "content": "👋 Goodbye! Feel free to return whenever you need assistance."})
        else:
            with st.chat_message("user"):
                st.write(query)
            
            st.session_state.chat_history.append({"role": "user", "content": query})
            
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                response_placeholder.write("🧠 Thinking...")
                
                with st.spinner("Processing your request..."):
                    response, tools_used = run_agent(query)
                    
                response_placeholder.empty()
                st.write(response)
                
                if tools_used:
                    with st.expander("🧰 Tools Used"):
                        for tool in tools_used:
                            st.info(f"**{tool}**")
            
            st.session_state.chat_history.append({"role": "assistant", "content": response, "tools_used": tools_used})

if __name__ == "__main__":
    main()