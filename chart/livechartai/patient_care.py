
from typing import Dict, List

import langchain
from langchain_openai import ChatOpenAI
from langchain_core.runnables.base import Runnable
from langchain_core.prompts import PromptTemplate
from django.db import models





# 1: get checklist from 1 doctor note -> checklist
#   - doctor note
# 2: validate care plan -> corrections & suggestions
#   - doctor notes list
#   - other notes list
#   - current care plan
# 3: Suggest update based on new information available
#   - doctor notes list
#   - other notes list
#   - current care plan

# get doctor notes sorted by time
# get other notes sorted by time
# get lab results sorted by time

# Objects:
# 
# PhysicianRole: doctor or resident
#   - name
#   - title
# 
# Physician:
#   - physician name
#   - doctor role (doctor or resident)

# NoteType:
#  - name (doctor, resident, lab result, care plan, generated care plan)
# 
# Note: 
#   - creator (physician)
#   - note_type (NoteType)
#   - datetime (auto now)
#   - text
#   

class Physician(models.Model):
    name = models.CharField(max_length=255)
    doctor_role = models.CharField(max_length=255, choices=[
        ("doctor", "Doctor"),
        ("resident", "Resident"),
    ])

class Patient(models.Model):
    name = models.CharField(max_length=255)

class Note(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    creator = models.ForeignKey(Physician, on_delete=models.CASCADE)
    note_type = models.CharField(max_length=255, choices=[
        ("doctor", "Doctor"),
        ("resident", "Resident"),
        ("lab_result", "Lab Result"),
        ("care_plan", "Care Plan"),
        ("generated_care_plan", "AI Generated Care Plan"),
    ])
    datetime = models.DateTimeField(auto_now_add=True)
    text = models.TextField()




PATIENT_CARE_TEMPLATE = """

You are an ICU doctor who is leading the care of a patient.

Your notes on this patient are:

--- Primary Doctor Notes ---
{doctor_notes}
---

Additional notes from other doctors and residents are:
---
{patient_notes}
---

{final_statement}
"""




def build_patient_care_chain(model_name: str, template: str, ) -> Runnable:
    """
    Contructs a runnable chain for processing .
    """
    model: ChatOpenAI = get_patient_care_model(model_name)
    prompt = PromptTemplate(
        template=template,
        input_variables=["doctor_notes", 'final_statement'],
        # partial_variables={
        #     "format_instructions": output_parser.get_format_instructions(),
        #     "criteria_list_text": build_criterion_list_text(criterion),
        #     "evaluator_name": model.model_name,
        # },
    )
    chain = prompt | model
    return chain


def get_patient_care_chain() -> Runnable:
    """
    Specifies the model, template, etc.
    used to construct a runnable chain.
    """
    model_name: str = 'gpt-4'
    template: str = PATIENT_CARE_TEMPLATE
    # criterion: dict = DEFAULT_EVAL_CRITERION
    # pydantic_parser = PydanticOutputParser(pydantic_object=Evaluation)

    chain = build_patient_care_chain(model_name, template)
    return chain


def get_patient_care_model(model_name: str, temperature: int = 0) -> ChatOpenAI:
    """
    Gets an instance of ChatOpenAI class for the model with a temperature of 0.
    """
    model = ChatOpenAI(model_name=model_name, temperature=temperature)
    return model

DOCTOR_NOTES = """
Mr. Smith, a 65-year-old male patient with a history of chronic heart failure, presents to the cardiology clinic with worsening dyspnea, fatigue, and peripheral edema. On examination, he exhibits signs of fluid overload, including elevated jugular venous pressure and bilateral lower extremity edema. Vital signs reveal a blood pressure of 100/70 mmHg, heart rate of 90 beats per minute, respiratory rate of 20 breaths per minute, and oxygen saturation of 94% on room air.
"""

CREATE_CHECKLIST_STATEMENT = "Create a checklist detailing what should do in the next 24 hours to care for the patient."

REVIEW_LATEST_NOTE = "Review the latest note on the patient and identify any errors and suggest necessary corrections."

REACT_TO_UPDATE_STATEMENT = "React to the latest update on the patient's condition and suggest any necessary changes to the care plan."


if __name__ == '__main__':
    chain = get_patient_care_chain()
    output = chain.invoke({"doctor_notes": DOCTOR_NOTES, 'final_statement': CREATE_CHECKLIST_STATEMENT})
    print(output)
    