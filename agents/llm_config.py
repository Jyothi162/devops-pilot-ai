
import os

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI


def get_llm():
    """
    Shared LLM configuration for DevOps Pilot AI.

    Local: Ollama
    Cloud: Groq
    """

    provider = os.getenv("LLM_PROVIDER", "ollama").lower()

    if provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is required when LLM_PROVIDER=groq"
            )

        return ChatOpenAI(
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
            temperature=0,
        )

    if provider == "ollama":
        return ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "llama3.2"),
            base_url=os.getenv(
                "OLLAMA_BASE_URL",
                "http://localhost:11434"
            ),
            temperature=0,
        )

    raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")
