from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

class ResearchResponse(BaseModel):
    header: str
    summary: str
    sources: list[str]
    tools_used: list[str]

llm = ChatOpenAI(model="o4-mini")
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a cybersecurity architect and analyst that will help analyze and help with rules for cybersecurity specialist.
            Answer them profesionally based on that they are specialist. Anwser to them directly without talking about it too much.
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        )
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())