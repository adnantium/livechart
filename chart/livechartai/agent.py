import os
import sys
from typing import Dict, List
import requests

from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse, PlainTextResponse, HTMLResponse
from langserve import add_routes

from livechartai.chain import (
    get_care_plan_chain,
    get_patient_data,
    get_observe_chain,
    get_ask_chain,
)

app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")



add_routes(
    app,
    get_care_plan_chain(),
    path="/care_plan",
)
add_routes(
    app,
    get_observe_chain(),
    path="/observe",
)


@app.post("/ask", response_class=PlainTextResponse)
async def ask_question(request: Request, question: str = Form(...)):
    answer = get_ask_chain(question).invoke(
        {
            "question": question,
        }
    )
    return answer


@app.get("/everything")
async def get_everything():
    patient_data = get_patient_data(app.patient_id)
    return {"patient_data": patient_data}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8888)
