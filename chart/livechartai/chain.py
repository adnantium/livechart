from typing import Dict, List
import requests




PATIENT_CARE_TEMPLATE = """

You are an ICU doctor who is leading the care of a patient.

{mission_statement}

{patient_data}

{final_statement}
"""

MISSION_STATEMENT = 'Your mission is to provide the best care for the patient.'

CREATE_CARE_PLAN_STATEMENT = 'Create a detailed checklist of what residents should do in the next 48 hours to care for the patient. Include any necessary tests, medications with doses, and interventions. Your response should only include the checklist.'

VALIDATE_CARE_PLAN_STATEMENT = """Validate the existing care plan in detail. Identify any errors, omissions and typos and list them under the heading "ERRORS!". 
Also provide any suggestions for improvement under the heading "SUGGESTIONS"."""

ANSWER_QUESTION_STATEMENT = 'Answer the following question in detail based on the current care plan and other patient notes: "{question}"'


from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


def get_patient_data(patient_id: int) -> Dict:
    patient_data = requests.get(f"http://localhost:8000/patient_data/{patient_id}/")
    return patient_data.text

def get_care_plan_chain():
    patient_id = 1
    model = ChatOpenAI(model_name='gpt-4', temperature=0)
    prompt = PromptTemplate(
        template=PATIENT_CARE_TEMPLATE,
        input_variables=[],
        partial_variables={
            'mission_statement': MISSION_STATEMENT,
            'patient_data': get_patient_data(patient_id),
            "final_statement": CREATE_CARE_PLAN_STATEMENT
        },
    )
    chain = prompt | model | StrOutputParser()
    return chain

def get_observe_chain():
    patient_id = 1
    model = ChatOpenAI(model_name='gpt-4', temperature=0)
    prompt = PromptTemplate(
        template=PATIENT_CARE_TEMPLATE,
        input_variables=[],
        partial_variables={
            'mission_statement': MISSION_STATEMENT,
            'patient_data': get_patient_data(patient_id),
            "final_statement": VALIDATE_CARE_PLAN_STATEMENT
        },
    )
    chain = prompt | model | StrOutputParser()
    return chain

# from langserve import CustomUserType
# from pydantic import BaseModel, RootModel
# class Question(RootModel):
#     root: str

def get_ask_chain(question: str):
    patient_id = 1
    model = ChatOpenAI(model_name='gpt-4', temperature=0)
    prompt = PromptTemplate(
        template=PATIENT_CARE_TEMPLATE,
        input_variables=['question',],
        partial_variables={
            # 'question': question,
            'mission_statement': MISSION_STATEMENT,
            'patient_data': get_patient_data(patient_id),
            "final_statement": ANSWER_QUESTION_STATEMENT.format(question=question),
        },
    )
    chain = prompt | model | StrOutputParser()
    # return chain.with_types(input_type=Question)
    return chain
