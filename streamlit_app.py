import streamlit as st
import openai

server = "OpenAI"

st.title("Azure GPT4")

# Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets[server]["API_KEY"]
openai.api_base = st.secrets[server]["BASE_URL"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # for response in openai.ChatCompletion.create(
        #     model=st.session_state["openai_model"],
        #     messages=[
        #         {"role": m["role"], "content": m["content"]}
        #         for m in st.session_state.messages
        #     ],
        #     stream=True,
        # ):
        #     full_response += response.choices[0].delta.get("content", "")
        #     message_placeholder.markdown(full_response + "▌")
        # message_placeholder.markdown(full_response)
    # st.session_state.messages.append({"role": "assistant", "content": full_response})
        response = openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
        )
        result = response.choices[0].message.content
        message_placeholder.markdown(result)
    st.session_state.messages.append({"role": "assistant", "content": result})
    # 转发的暂时用不了openai streaming，这里改写一下，可以用了再改呗