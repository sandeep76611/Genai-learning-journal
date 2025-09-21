import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate, FewShotPromptTemplate

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize LLM
llm = ChatGroq(
    model="LLaMA3-70b-8192",
    api_key=GROQ_API_KEY,
)

# Examples: input (job description) and expected output (skills)
examples = [
    {
        "JobDescription": "We are looking for a Data Analyst who is proficient in SQL, Python, and data visualization tools like Tableau.",
        "Skills": "SQL, Python, Tableau, Data Visualization"
    },
    {
        "JobDescription": "The candidate should have strong knowledge in Java, Spring Boot, and cloud technologies such as AWS.",
        "Skills": "Java, Spring Boot, AWS, Cloud Computing"
    },
    {
        "JobDescription": "Seeking a Frontend Developer with expertise in React, JavaScript, HTML, and CSS.",
        "Skills": "React, JavaScript, HTML, CSS, Frontend Development"
    },
]

# Define how each example looks
example_prompt = PromptTemplate(
    input_variables=["JobDescription", "Skills"],
    template="Job Description: {JobDescription}\nExtracted Skills: {Skills}\n"
)

# Few-shot template
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="Job Description: {JobDescription}\nExtracted Skills:",
    input_variables=["JobDescription"]
)

# Example input (new job description)
new_jd = """We are hiring a Machine Learning Engineer skilled in Python, TensorFlow, deep learning, and cloud platforms like GCP."""
formatted_prompt = few_shot_prompt.format(JobDescription=new_jd)

# Get response
response = llm.invoke(formatted_prompt)
print("Extracted Skills:\n", response.content)