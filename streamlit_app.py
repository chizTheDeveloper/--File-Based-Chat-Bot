import os
import PyPDF2
import streamlit as st
from io import StringIO
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import Any, Dict, List
import random
import string


st.set_page_config(page_title="Chima Chat Bot", page_icon="🤖")


with st.sidebar:
    api_key = st.text_input("API Key", key="file_qa_api_key", type="password")
    os.environ["OPENAI_API_KEY"] =  api_key

loaded_text = ""

@st.cache_data
def load_docs(files):
    st.info("`Reading doc ...`")
    all_text = ""
    for file_path in files:
        file_extension = os.path.splitext(file_path.name)[1]
        if file_extension == ".pdf":
            pdf_reader = PyPDF2.PdfReader(file_path)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            all_text += text
        elif file_extension == ".txt":
            stringio = StringIO(file_path.getvalue().decode("utf-8"))
            text = stringio.read()
            all_text += text
        else:
            st.warning('Please provide txt or pdf.', icon="⚠️")
    return all_text


@st.cache_resource
def split_texts(text, chunk_size, overlap, split_method):

    # Split texts
    # IN: text, chunk size, overlap, split_method
    # OUT: list of str splits

    split_method = "RecursiveTextSplitter"
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=overlap)

    splits = text_splitter.split_text(text)
    if not splits:
        st.error("Failed to split document")
        st.stop()

    return splits


# ...
def run_llm(query: str, chat_history: List[Dict[str, Any]] = [], splits: List[str] = []):
    # Embed using OpenAI embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    vectorstore = FAISS.from_texts(splits, embeddings)

    retriever = vectorstore.as_retriever(k=5)
    chat_openai = ChatOpenAI(verbose=True, temperature=0)

    qa = ConversationalRetrievalChain.from_llm(
        llm=chat_openai, retriever=retriever, return_source_documents=True
    )

    return qa({"question": query, "chat_history": chat_history})


def main():
    if (
            "chat_answers_history" not in st.session_state
            and "user_prompt_history" not in st.session_state
            and "chat_history" not in st.session_state
    ):
        st.session_state["chat_answers_history"] = []
        st.session_state["user_prompt_history"] = []
        st.session_state["chat_history"] = []

    st.write(
        f"""
        <div style="display: flex; align-items: center; margin-left: 0;">
            <p><h1 style="display: inline-block;">Chima's Chat Bot</h1></p>
        </div>
        <div style="display: flex; align-items: center; margin-left: 0;">
            <p><h3 style="display: inline-block;">Upload a file and chat </h3></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    splitter_type = "RecursiveCharacterTextSplitter"

    uploaded_files = st.file_uploader("Upload a PDF or TXT Document", type=[
        "pdf", "txt"], accept_multiple_files=True)

    if uploaded_files and not api_key:
        st.info("Please add your API key to continue.")

    if uploaded_files and api_key:
        if 'last_uploaded_files' not in st.session_state or st.session_state.last_uploaded_files != uploaded_files:
            st.session_state.last_uploaded_files = uploaded_files
            if 'eval_set' in st.session_state:
                del st.session_state['eval_set']

        loaded_text = load_docs(uploaded_files)
        splits = split_texts(loaded_text, chunk_size=1000,
                             overlap=50, split_method=splitter_type)

        st.write("Ready to answer questions.")

        prompt = st.text_input("Prompt", placeholder="Enter your question here...") or st.button(
            "Submit"
        )

        if prompt:
            with st.spinner("Generating response..."):
                generated_response = run_llm(
                    query=prompt, chat_history=st.session_state["chat_history"], splits=splits
                )

                formatted_response = (
                    f"{generated_response['answer']}"
                )

                st.session_state.chat_history.append(
                    (prompt, generated_response["answer"]))
                st.session_state.user_prompt_history.append(prompt)
                st.session_state.chat_answers_history.append(formatted_response)

        if st.session_state["chat_answers_history"]:
            for generated_response, user_query in zip(
                    st.session_state["chat_answers_history"],
                    st.session_state["user_prompt_history"],
            ):
                res_user = ''.join(random.choices(string.ascii_letters, k=5))
                st.chat_message("user", avatar="🤨").write(user_query, key=res_user)

                res_chatbot = ''.join(random.choices(string.ascii_letters, k=5))
                st.chat_message("chatbot", avatar="🤖").write(generated_response, key=res_chatbot)


if __name__ == "__main__":
    main()
