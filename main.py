# The main Streamlit Python code

import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# Load API Key from .env file (for local development)
load_dotenv()

# Initialize the Groq client
# Streamlit will first look for secrets in .streamlit/secrets.toml, then environment variables
api_key = os.getenv("GROQ_API_KEY")

# Streamlit UI Setup
st.set_page_config(page_title="Professional Email Generator", page_icon="✉️", layout="centered")

st.title("✉️ AI Professional Email Generator")
st.write("Generate perfectly structured business, formal, or casual emails in seconds.")

# Side Bar for API key configuration if not set in environment
if not api_key:
    st.sidebar.warning("API Key not found!")
    api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")
else:
    st.sidebar.success("Groq API Key is configured and ready!")

# Input fields for the User
st.subheader("Email Parameters")

col1, col2 = st.columns(2)
with col1:
    sender = st.text_input("Your Name (Sender):", placeholder="e.g., John Doe")
    recipient = st.text_input("Recipient's Name/Role:", placeholder="e.g., Hiring Manager")
with col2:
    subject_matter = st.text_input("Email Subject/Topic:", placeholder="e.g., Asking for leave, Follow-up")
    tone = st.selectbox("Select Email Tone:", ["Professional", "Formal", "Casual", "Urgent", "Apologetic"])

key_points = st.text_area(
    "Key Points to Include:", 
    placeholder="Write the core message in bullet points or simple sentences. For example:\n- Need leave on Friday for a medical checkup\n- Will hand over pending tasks to Sarah"
)

# Generation Button
if st.button("Generate Email 🚀"):
    if not api_key:
        st.error("Please provide a valid Groq API Key to proceed.")
    elif not sender or not recipient or not subject_matter or not key_points:
        st.warning("Please fill in all the input fields before generating.")
    else:
        with st.spinner("Writing your email..."):
            try:
                # 1. Initialize client
                client = Groq(api_key=api_key)
                
                # 2. DEFINE THE PROMPT TEMPLATE (Directly answers Viva Q#6!)
                prompt_template = f"""
                You are an expert executive assistant specializing in professional communications.
                Write an email based on the following details:
                
                - **Sender**: {sender}
                - **Recipient**: {recipient}
                - **Topic/Subject**: {subject_matter}
                - **Tone**: {tone}
                - **Key Information/Points**: 
                {key_points}
                
                Guidelines:
                1. Write a professional Subject line at the very beginning of your response.
                2. Match the selected tone ("{tone}") precisely.
                3. Keep the email concise, polite, and grammatically perfect.
                4. Do not include any placeholder brackets in your output (e.g. [Your Name]). Use the provided names.
                """
                
                # 3. Call the Groq LLM API
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",  # Updated to the current Llama 3.1 model
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a professional business writing assistant."
                        },
                        {
                            "role": "user",
                            "content": prompt_template
                        }
                    ],
                    temperature=0.7,
                    max_tokens=1024
                )
                
                # 4. Display the Output
                generated_email = response.choices[0].message.content
                st.subheader("✨ Generated Email Draft")
                st.info("You can copy the generated email below:")
                st.text_area("", value=generated_email, height=350)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
