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

# Prompt template for movie recommendations
template = """
You are a movie recommendation assistant. 
Suggest 5 movies that belong to the genre: {genre}.
Only list the movie names, nothing else.
"""

prompt = PromptTemplate(
    input_variables=["genre"],
    template=template,
)

# Example: Ask for Science Fiction movies
genre_input = "Science Fiction"
formatted_prompt = prompt.format(genre=genre_input)

response = llm.invoke(formatted_prompt)
print("Recommended Movies:\n", response.content)
