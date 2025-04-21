import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph,START,END
from tavily import TavilyClient
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage,SystemMessage,AIMessage,HumanMessage
import requests
from bs4 import BeautifulSoup
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
os.environ["TAVILY_API_KEY"] = os.getenv('TAVILY_API_KEY')
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

llm = ChatGroq(model='llama-3.3-70b-versatile',api_key=os.environ['GROQ_API_KEY'])

## Defining the state
class State(TypedDict):
    messages : Annotated[list[BaseMessage],add_messages]
    docs : list[str]
    answer : str

graph_builder = StateGraph(State)

## Function for Web Crawling
def fetch_web_data(state:State, max_results: int = 5) -> dict:
    client = TavilyClient(api_key=os.environ['TAVILY_API_KEY'])
    query = state['messages'][-1].content
    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results
    )
    # print(response)
    result = response['results']
    urls = [res["url"] for res in result]
    docs = []
    for url in urls:
        try:
            html = requests.get(url, timeout=5).text
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text(separator="\n").strip()
            docs.append(text[:500])
        except Exception:
            docs.append("Failed to fetch content.")
    return {
        "messages": [HumanMessage(content=f"Search done for: {query}")],
        'docs':docs
    }

## Function for answer drafter
def draft_answer(state: State) -> dict:
    docs = state["docs"]
    query = state['messages'][-1]
    docs_string = "\n\n".join(docs)
    prompt = ChatPromptTemplate.from_messages([
        ('system','You are the assistant who summarize the answer from the docs accordin to the user query.'),
        ('user','user quer is {query} and docs are {docs_string}.')
    ])
    format_message = prompt.format_messages(query=query,docs_string=docs_string)
    response = llm.invoke(format_message)
    
    return {
        "messages": [AIMessage(content=response.content)],
        "answer": response.content
    }

## Defining the Graph
graph = StateGraph(State)
graph.add_node("crawl", fetch_web_data)
graph.add_node("draft", draft_answer)

graph.set_entry_point("crawl")
graph.add_edge("crawl", "draft")
graph.add_edge("draft", END)

app = graph.compile()


def ask_query():
    query = input('Ask you Question:')
    initial_state = {
        "messages": [
            HumanMessage(content=query)
        ],
        "docs": [],
        "answer": ""
    }

    final_state = app.invoke(initial_state)

    print(final_state['answer'])
    
ask_query()
