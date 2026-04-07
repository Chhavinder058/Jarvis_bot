#!/usr/bin/env python
# coding: utf-8

# Step 1: Imports and Configuration

# In[5]:


import streamlit as st
import ollama

st.set_page_config(page_title="my app", page_icon=":guardsman:", layout="wide")
st.title("Jarvis")
st.caption("Running on Ollama 3.2 - No data leaves the device")


# Step 2: Memory

# In[6]:


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "You are a helpful assistant."}
    ]


# In[7]:


# Display chat messages from history on app rerun
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message(msg["role"]).write(msg["content"])
    else:
        st.chat_message(msg["role"]).write(msg["content"])


# In[8]:


# Handle user input
if prompt := st.chat_input("What is on your mind?"):
    # 1. Display user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 2. Placeholder for the AI response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        # 3. Call the Local Model
        # We use 'stream=True' so the text types out like in ChatGPT
        stream = ollama.chat(
            model='llama3.2',
            messages=[{'role': 'user', 'content': prompt}],
            stream=True,
        )

        # 4. Process the stream
        for chunk in stream:
            if chunk['message']['content']:
                content = chunk['message']['content']
                full_response += content
                response_placeholder.markdown(full_response + "▌")

        # Final update to remove the cursor
        response_placeholder.markdown(full_response)

    # 5. Save the AI's response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

