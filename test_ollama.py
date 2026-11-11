
from agents.llm_config import get_llm


def main():
    print("\nTesting Ollama Llama 3.2...\n")

    llm = get_llm()

    response = llm.invoke(
        "A worker service has CPU usage of 92% "
        "and database connection timeouts. "
        "Suggest possible causes in three short points."
    )

    print(response.content)


if __name__ == "__main__":
    main()
