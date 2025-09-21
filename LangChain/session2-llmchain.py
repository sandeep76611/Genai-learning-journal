import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

llm=ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=api_key,
    temperature=0.1,
)

prompt_explain=PromptTemplate(
    input_variables=["topic"],
    template="explain the topic {topic} in simple words"
)

prompt = PromptTemplate(
    input_variables=["product", "audience"],
    template="write a marketing email to {audience} about {product}"
)


explain_chain = LLMChain(llm=llm,prompt=prompt_explain)
marketing_chain = LLMChain(llm=llm,prompt=prompt)

result1 = explain_chain.run({"topic":"Quantum Computing"})
result2 = marketing_chain.run({"product":"LangChain","audience":"developers"})
       
print(" \n Explanation Chain Result: \n", result1)
print("\n Marketing Chain Result: \n", result2)