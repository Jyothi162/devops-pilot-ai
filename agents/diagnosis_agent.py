
from agents.state import DevOpsState
from agents.llm_config import get_llm


def diagnosis_agent(state: DevOpsState) -> dict:
    """
    Analyze infrastructure metrics and application logs
    using the configured LLM.

    Identify possible root causes without claiming
    that unverified hypotheses are confirmed.
    """

    metrics = state.get("infrastructure_result", {})
    logs = state.get("log_result", {})

    print("[Diagnosis Agent] Analyzing incident...")

    prompt = f"""
You are an experienced DevOps incident analyst.

Analyze the following simulated incident.

Infrastructure metrics:
{metrics}

Application logs:
{logs}

Instructions:
1. Identify up to three possible root causes.
2. Explain how the metrics and logs support each cause.
3. Identify what additional evidence is needed.
4. Do not claim a root cause is confirmed without proof.
5. Distinguish observations from hypotheses.
6. Do not execute commands or suggest destructive actions.
7. Do not assume a particular database technology
   unless it is explicitly identified in the evidence.
8. Clearly state when evidence is insufficient.

Provide a concise technical diagnosis.
"""

    llm = get_llm()
    response = llm.invoke(prompt)

    return {
        "diagnosis": response.content
    }
