# PydanticOutputParser

import os 
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

class Person(BaseModel):
    name: str = Field(description="The name of the person")
    age: int = Field(description="The age of the person")
    city: str = Field(description="The city where the person lives")
    
parser = PydanticOutputParser(pydantic_object=Person)

prompt=PromptTemplate(
    input_variables=["input"],
    template="Extract the name, age, and city from the following text: \n{input}\n{format_instructions}",
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=api_key)

input_text="my name is Jerin and i am 24 years old and i live in chennai"

formatted_prompt = prompt.format(input=input_text)

response = llm.invoke(formatted_prompt)

parsed = parser.parse(response.content)

print(parsed)

print(parsed.name)
print(parsed.age)

# CommaSeperatedListOutputParser

from langchain.output_parsers import CommaSeparatedListOutputParser

parser1 = CommaSeparatedListOutputParser()

prompt1=PromptTemplate(
    input_variables=[],
    template="List out top 5 programing languages.\n{format_instructions}",
    partial_variables={"format_instructions":parser1.get_format_instructions()},
)


# llm1 = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=api_key)

formatted_prompt1=prompt1.format()

response1 = llm.invoke(formatted_prompt1)

print(response1.content)

parsed = parser1.parse(response1.content)

print(f"List:{parsed}")