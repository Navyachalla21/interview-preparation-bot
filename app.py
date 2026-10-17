import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Connect to the Gemini language model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key
)

# Create a prompt template to shape the AI's behavior as an Interview Prep assistant
prompt_template = PromptTemplate(
    input_variables=["question"],
    template="""You are an Interview Preparation Assistant. Your job is to help users
prepare for job interviews by answering questions about common interview questions,
how to structure good answers, behavioral interview techniques (like the STAR method),
technical interview tips, and general interview advice.

If the user asks something completely unrelated to interviews or job preparation,
politely redirect them back to interview-related topics.

User's question: {question}

Your response:"""
)

# Streamlit app interface
st.title("🎯 Interview Preparation Bot")
st.write("Ask me anything about interview preparation — common questions, answer structure, behavioral techniques, and more!")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

user_question = st.text_input("Enter your interview-related question:")

if user_question:
    try:
        final_prompt = prompt_template.format(question=user_question)
        response = llm.invoke(final_prompt)

        content = response.content
        if isinstance(content, list):
            answer = "\n".join(
                block.get("text", "") for block in content
                if isinstance(block, dict) and block.get("type") == "text"
            )
        else:
            answer = content

        st.session_state.history.append((user_question, answer))
    except Exception as e:
        st.error(f"Something went wrong: {e}")

# Display all Q&A pairs, most recent first
for q, a in reversed(st.session_state.history):
    st.write(f"**Q: {q}**")
    st.write(a)
    st.write("---")