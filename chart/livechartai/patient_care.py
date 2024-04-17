import os
import sys
from typing import Dict, List

import langchain
from langchain_openai import ChatOpenAI
from langchain_core.runnables.base import Runnable
from langchain_core.prompts import PromptTemplate
import django

# project_path = "path/to/project/dir"
sys.path.append(".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chart.settings")
django.setup()

from icu.models import CareTaker, Note, Patient


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


PATIENT_CARE_TEMPLATE = """

You are an ICU doctor who is leading the care of a patient: {patient_info}

--- Primary Doctor Notes ---
{doctor_notes}
---

--- Additional notes ---
{patient_notes}
---

{final_statement}
"""


def build_patient_care_chain(
    model_name: str,
    template: str,
) -> Runnable:
    """
    Contructs a runnable chain for processing .
    """
    model: ChatOpenAI = get_patient_care_model(model_name)
    prompt = PromptTemplate(
        template=template,
        input_variables=["doctor_notes", "final_statement"],
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
    model_name: str = "gpt-4"
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


def get_patient_info(patient: Patient) -> str:
    """
    Returns a string representation of the patient's info.
    """
    patient_info = f"Name: {patient.name} Admission Date: {patient.admission_datetime}"
    return patient_info


def get_patient_notes(patient: Patient, roles_include=None, roles_exclude=None) -> str:
    """
    Returns a string representation of the patient's notes.
    """
    notes = Note.objects.filter(patient=patient).order_by("-datetime")
    if roles_include:
        notes = notes.filter(creator__role__in=roles_include)
    if roles_exclude:
        notes = notes.exclude(creator__role__in=roles_exclude)
    notes_str = "\n" + "-" * 20 + "\n"
    for note in notes:
        note_dt = note.datetime.strftime("%Y-%m-%d %H:%M:%S")
        notes_str += f"{note.creator.name} - {note_dt}\n{note.text}\n"
        notes_str += "-" * 20 + "\n\n"
    return notes_str


# Mr. Smith, a 65-year-old male patient with a history of chronic heart failure, presents to the cardiology clinic with worsening dyspnea, fatigue, and peripheral edema. On examination, he exhibits signs of fluid overload, including elevated jugular venous pressure and bilateral lower extremity edema. Vital signs reveal a blood pressure of 100/70 mmHg, heart rate of 90 beats per minute, respiratory rate of 20 breaths per minute, and oxygen saturation of 94% on room air.

CREATE_CHECKLIST_STATEMENT = "Create a checklist of what residents should do in the next 24 hours to care for the patient. Include any necessary tests, medications, and interventions."

REVIEW_LATEST_NOTE = "Review the latest note on the patient and identify any errors and suggest necessary corrections."

REACT_TO_UPDATE_STATEMENT = "React to the latest update on the patient's condition and suggest any necessary changes to the care plan."


if __name__ == "__main__":

    patient_id = 1
    patient = Patient.objects.get(id=patient_id)
    # print(patient)
    patient_info = get_patient_info(patient)
    print(patient_info)
    doctor_notes = get_patient_notes(patient, roles_include=["doctor"])
    print(doctor_notes)
    patient_notes = get_patient_notes(patient, roles_exclude=["doctor"])
    print(patient_notes)

    chain = get_patient_care_chain()
    output = chain.invoke(
        {
            "doctor_notes": doctor_notes,
            "patient_info": patient_info,
            "patient_notes": patient_notes,
            "final_statement": CREATE_CHECKLIST_STATEMENT,
        }
    )
    print(output.content)
