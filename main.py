from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor

from tools import search_tool, wiki_tool, save_tool

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
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, wiki_tool, save_tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
query = input("What do you want to help with cyber?")
raw_response = agent_executor.invoke({"query": query})

output = raw_response.get("output")
if isinstance(output, list):
    output = "".join(block.get("text", "") for block in output)

try:
    structured_response = parser.parse(output)
    print(structured_response)
except Exception as e:
    print("Error parsing response,", e, "Raw Response - ", raw_response)