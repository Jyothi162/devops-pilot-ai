
from fastapi import FastAPI
from pydantic import BaseModel, Field
from starlette.concurrency import run_in_threadpool
from langfuse.langchain import CallbackHandler

from agents.graph import graph


app = FastAPI(
    title="DevOps Pilot AI",
    description="Multi-Agent DevOps Automation Platform",
    version="0.2.0",
)


class InvestigationRequest(BaseModel):
    user_request: str = Field(min_length=1)
    service_name: str = Field(min_length=1)


@app.get("/")
def home():
    return {
        "message": "Welcome to DevOps Pilot AI",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/investigate")
async def investigate(request: InvestigationRequest):
    initial_state = {
        "user_request": request.user_request,
        "service_name": request.service_name,
        "investigation_plan": "",
        "next_agent": "",
        "infrastructure_result": {},
        "log_result": {},
        "diagnosis": "",
        "remediation": "",
        "approved": False,
        "final_response": "",
    }

    langfuse_handler = CallbackHandler()

    result = await run_in_threadpool(
        graph.invoke,
        initial_state,
        config={"callbacks": [langfuse_handler]},
    )

    return {
        "service_name": request.service_name,
        "investigation_plan": result.get("investigation_plan", ""),
        "infrastructure_result": result.get("infrastructure_result", {}),
        "log_result": result.get("log_result", {}),
        "diagnosis": result.get("diagnosis", ""),
        "remediation": result.get("remediation", ""),
        "approved": result.get("approved", False),
    }
