
import os

from langchain_ollama import ChatOllama


def get_llm():
    """
    Create a shared LLM instance for DevOps Pilot AI.

    Default provider: Local Ollama
    Default model: Llama 3.2
    """

    model_name = os.getenv("OLLAMA_MODEL", "llama3.2")

    base_url = os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434"
    )

    return ChatOllama(
        model=model_name,
        temperature=0,
        base_url=base_url
    )
