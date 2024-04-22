from typing import Dict, List
import requests


PATIENT_CARE_TEMPLATE = """
You are an ICU doctor who is leading the care of a patient.

{mission_statement}

{patient_data}

{final_statement}
"""

MISSION_STATEMENT = (
    "Your mission is to provide the best care possible for your patient."
)

CREATE_CARE_PLAN_STATEMENT = "Create a detailed checklist of what residents should do in the next 48 hours to care for the patient. Ignore the existing care plan and suggest an updated one based on latest notes and updates. Include any necessary tests, medications with doses, and interventions. Your response should only include the checklist."

OBSERVE_PATIENT_STATEMENT = """Review all the information you have about the patient and identify any potential issues.
Ensure that you check for any recent updates to patients notes that require action. Check for:
    * medical errors
    * omissions
    * typos
    * recent updates that require urgent action

Your output should be a bullet list of any issues that you find. Each item in the checklist should indicate its urgency as "High", "Medium", or "Low"."""

ANSWER_QUESTION_STATEMENT = 'Answer the following question in detail based on the current care plan and other patient notes: "{question}"'


from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def get_patient_data(patient_id: int) -> Dict:
    patient_data = requests.get(f"http://localhost:8000/patient_data/{patient_id}/")
    return patient_data.text


def get_care_plan_chain():
    patient_id = 1
    model = ChatOpenAI(model_name="gpt-4", temperature=0)
    prompt = PromptTemplate(
        template=PATIENT_CARE_TEMPLATE,
        input_variables=[],
        partial_variables={
            "mission_statement": MISSION_STATEMENT,
            "patient_data": get_patient_data(patient_id),
            "final_statement": CREATE_CARE_PLAN_STATEMENT,
        },
    )
    chain = prompt | model | StrOutputParser()
    return chain


def get_observe_chain():
    patient_id = 1
    patient_data = get_patient_data(patient_id)
    model = ChatOpenAI(model_name="gpt-4", temperature=0)
    prompt = PromptTemplate(
        template=PATIENT_CARE_TEMPLATE,
        input_variables=[],
        partial_variables={
            "mission_statement": MISSION_STATEMENT,
            "patient_data": patient_data,
            "final_statement": OBSERVE_PATIENT_STATEMENT,
        },
    )
    chain = prompt | model | StrOutputParser()
    return chain

def get_ask_chain(question: str):
    patient_id = 1
    model = ChatOpenAI(model_name="gpt-4", temperature=0)
    prompt = PromptTemplate(
        template=PATIENT_CARE_TEMPLATE,
        input_variables=[
            "question",
        ],
        partial_variables={
            # 'question': question,
            "mission_statement": MISSION_STATEMENT,
            "patient_data": get_patient_data(patient_id),
            # NOTE: This is a little clunk but LC templates don't seem to do nested variables
            "final_statement": ANSWER_QUESTION_STATEMENT.format(question=question),
        },
    )
    chain = prompt | model | StrOutputParser()
    return chain
