from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage, SystemMessage
import os

cohere_api_key = os.environ.get("COHERE_API_KEY")

def create_cohere_client():
    return ChatCohere(model="command-r", cohere_api_key=cohere_api_key)

def create_search_query(topic: str, motivation: str, source: str) -> str:
    """
    Creates a search query
    """
    llm = create_cohere_client()
    system_message = SystemMessage("You are a language model specialized in creating search queries. Your goal is to generate a search query that will help the user find relevant information regarding their topic of interest, why they are interested in the topic, with respect to the specific source. You must only return the search query or the system will break.")
    prompt = f"Create a search query to find relevant information about {topic} because {motivation} from {source}. Do not attach quotes to the search query."
    human_message = HumanMessage(prompt)
    response = llm.invoke([system_message, human_message])
    return response.content

def summarize(text: str) -> str:
    """Summarizes text"""
    llm = create_cohere_client()
    system_message = SystemMessage("You are a language model specialized in summarizing content concisely and clearly. Your goal is to extract the key points and present them in a way that is easy to digest.")
    prompt = f"""
    You are a language model specialized in summarizing content. Your task is to read the provided transcript and create a clear, and concise summary suitable for a quick glance. Focus on the main points and essential details discussed in the transcript.

    Here is the text to summarize:

    {text}
    """
    human_message = HumanMessage(prompt)
    response = llm.invoke([system_message, human_message])
    return response.content
