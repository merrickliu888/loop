from sources import sources as source_list
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
    system_message = SystemMessage("You are a language model specialized in creating search queries. Your goal is to generate a search query that will help the user find relevant information regarding their topic of interest, why they are interested in the topic, with respect to the specific source.")
    prompt = f"Create a search query to find relevant information about {topic} because {motivation} from {source}."
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

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    print(cohere_api_key)
    x = summarize("Alexander III of Macedon (Ancient Greek: Ἀλέξανδρος, romanized: Alexandros; 20/21 July 356 BC – 10/11 June 323 BC), most commonly known as Alexander the Great,[c] was a king of the ancient Greek kingdom of Macedon.[d] He succeeded his father Philip II to the throne in 336 BC at the age of 20 and spent most of his ruling years conducting a lengthy military campaign throughout Western Asia, Central Asia, parts of South Asia, and Egypt. By the age of 30, he had created one of the largest empires in history, stretching from Greece to northwestern India.[1] He was undefeated in battle and is widely considered to be one of history's greatest and most successful military commanders.[2][3][4]")
    print(x)
    y = create_search_query("Alexander the Great", "I'm interested in ancient history", "Arvix")
    print(y)