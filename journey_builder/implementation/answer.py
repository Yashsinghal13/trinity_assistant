# from pathlib import Path
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_chroma import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_core.messages import SystemMessage, HumanMessage, convert_to_messages
# from langchain_core.documents import Document
# from langchain_google_genai import ChatGoogleGenerativeAI



# from dotenv import load_dotenv


# load_dotenv(override=True)

# #MODEL = "gpt-5-nano"
# MODEL = "gemini-2.5-flash"   # fast & cheap

# DB_NAME = str(Path(__file__).parent.parent / "codebase"/ "vector_db")

# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# #embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
# RETRIEVAL_K = 10

# SYSTEM_PROMPT = """
# You are a knowledgeable, friendly assistant representing the company Octro.
# You are chatting with a user about Trinity CRM Platform.
# If relevant, use the given context to answer any question.
# If you don't know the answer, only Say "I don't know" and Please Ask related to the Trinity.
# Context:
# {context}
# """

# vectorstore = Chroma(persist_directory=DB_NAME, embedding_function=embeddings)
# retriever = vectorstore.as_retriever()
# #llm = ChatOpenAI(temperature=0, model_name=MODEL)
# llm = ChatGoogleGenerativeAI(
#     model=MODEL,
#     temperature=0
# )


# def fetch_context(question: str) -> list[Document]:
#     """
#     Retrieve relevant context documents for a question.
#     """
#     return retriever.invoke(question, k=RETRIEVAL_K)


# def combined_question(question: str, history: list[dict] = []) -> str:
#     """
#     Combine all the user's messages into a single string.
#     """
#     prior = "\n".join(m["content"] for m in history if m["role"] == "user")
#     return prior + "\n" + question


# def answer_question(question: str, history: list[dict] = []) -> tuple[str, list[Document]]:
#     """
#     Answer the given question with RAG; return the answer and the context documents.
#     """
#     combined = combined_question(question, history)
#     docs = fetch_context(combined)
#     context = "\n\n".join(doc.page_content for doc in docs)
#     system_prompt = SYSTEM_PROMPT.format(context=context)
#     messages = [SystemMessage(content=system_prompt)]
#     messages.extend(convert_to_messages(history))
#     messages.append(HumanMessage(content=question))
#     response = llm.invoke(messages)
#     return response.content, docs


from pathlib import Path
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from openai import OpenAI
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage, convert_to_messages
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from db import get_report_by_planner_id, listing_all_journey
import json
load_dotenv(override=True)



GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
google_api_key = os.getenv("GOOGLE_API_KEY")
# client = OpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)
OLLAMA_BASE_URL = os.getenv("OLLAMA_URL")
client = OpenAI(base_url=OLLAMA_BASE_URL, api_key='ollama')
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_report_by_planner_id",
            "description": "Get the Metrics by planner id",
            "parameters": {
                "type": "object",
                "properties": {
                    "planner_id": {"type": "integer"}
                },
                "required": ["planner_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "listing_all_journey",
            "description": "It will List down all the journey with given status",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {"type": "string"}
                },
                "required": ["status"]
            }
        }
    }

]

#MODEL = "gpt-5-nano"
# MODEL = "gemini-2.5-flash"   # fast & cheap
MODEL="llama3.2"

DB_NAME = "/Users/yashsinghal/trinity_helper_chatbot/journey_builder/codebase/vector_db"

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
RETRIEVAL_K = 10


SYSTEM_PROMPT = """
You are a knowledgeable, friendly assistant representing the company Octro.
You are chatting with a user about Trinity CRM Platform.
If relevant, use the given context to answer any question.
If you don't know the answer, only Say "I don't know". Please Ask Question related to the Trinity.
Context:
{context}
"""

vectorstore = Chroma(persist_directory=DB_NAME, embedding_function=embeddings)
retriever = vectorstore.as_retriever()

def normalize_tool_args(args: dict):
    clean = {}
    for k, v in args.items():
        if isinstance(v, dict) and "value" in v:
            clean[k] = v["value"]
        else:
            clean[k] = v
    return clean


def fetch_context(question: str) -> list[Document]:
    """
    Retrieve relevant context documents for a question.
    """
    return retriever.invoke(question, k=RETRIEVAL_K)


def combined_question(question: str, history: list[dict] = []) -> str:
    """
    Combine all the user's messages into a single string.
    """
    prior = "\n".join(m["content"] for m in history if m["role"] == "user")
    return prior + "\n" + question


def convert_messages(messages):
    formatted = []
    for msg in messages:
        if isinstance(msg, SystemMessage):
            formatted.append({"role": "system", "content": msg.content})
        elif isinstance(msg, HumanMessage):
            formatted.append({"role": "user", "content": msg.content})
    return formatted


def answer_question(question: str, history: list[dict] = []):
    combined = combined_question(question, history)
    docs = fetch_context(combined)
    context = "\n\n".join(doc.page_content for doc in docs)

    system_prompt = SYSTEM_PROMPT.format(context=context)

    messages = [
        {"role": "system", "content": system_prompt}
    ]

    # Add history
    for m in history:
        messages.append({
            "role": m["role"],
            "content": m["content"]
        })

    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools
    )

    message = response.choices[0].message
    print("LLM Response:", message.content)

    if message.tool_calls:
        print("Yes")
        tool_call = message.tool_calls[0]
        arguments = json.loads(tool_call.function.arguments)
        arguments = normalize_tool_args(arguments)
        print("Tool Call:", tool_call.function.name, arguments)
        result = None
        function_name = tool_call.function.name

        if function_name == "get_report_by_planner_id":
            result = get_report_by_planner_id(**arguments)
        elif function_name == "listing_all_journey":
            result = listing_all_journey(**arguments)

        second_response = client.chat.completions.create(
            model=MODEL,
            messages=messages + [
                {
                    "role": "assistant",
                    "tool_calls": message.tool_calls
                },
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                }
            ]
        )

        return second_response.choices[0].message.content, docs

    return message.content, docs

#answer_question("generate a report for planner id 252")


