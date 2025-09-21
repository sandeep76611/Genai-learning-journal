import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize LLM
llm = ChatGroq(
    model="LLaMA3-70b-8192",
    api_key=GROQ_API_KEY,
)

# Define the prompt template
template = """
You are an HR expert. 
Generate 5 to 7 interview questions for the job role: {job_role}.
Do not add answers or extra explanation, only list the questions.
"""

prompt = PromptTemplate(
    input_variables=["job_role"],
    template=template,
)

# Example: Job role input
job = "Software developer"
formatted_prompt = prompt.format(job_role=job)

# Get response
response = llm.invoke(formatted_prompt)
print("Interview Questions for", job, ":\n")
print(response.content)
