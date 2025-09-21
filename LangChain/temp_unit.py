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


# Examples for few-shot learning
examples = [
    {"Temperature": "0 Celsius", "Converted": "32 Fahrenheit, 273.15 Kelvin"},
    {"Temperature": "100 Celsius", "Converted": "212 Fahrenheit, 373.15 Kelvin"},
    {"Temperature": "25 Celsius", "Converted": "77 Fahrenheit, 298.15 Kelvin"},
]

# Example format
example_prompt = PromptTemplate(
    input_variables=["Temperature", "Converted"],
    template="Input: {Temperature}\nOutput: {Converted}\n"
)

# Few-shot template
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="Input: {Temperature}\nOutput:",
    input_variables=["Temperature"]
)

# Example usage
new_temp = "50 Celsius"
formatted_prompt = few_shot_prompt.format(Temperature=new_temp)

response = llm.invoke(formatted_prompt)
print("Converted:\n", response.content)
