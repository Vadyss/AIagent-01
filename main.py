from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatMessagePromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

llm = ChatOpenAI(model="o4-mini")