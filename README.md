

An experiment to test the capabilities of an LLM to assist ICU teams in creating task lists, reporting patient status, and identifying errors and oversights.

The traditional medical chart is reimagined as an LLM agent, tasked with managing patient care using all accessible patient information.

### Example Outputs

Here are some examples of errors and oversights that it was able to detect:

> Urgent: The dosage for Furosemide is listed as "606 mg IV twice daily". This is a typographical error as the usual dose of Furosemide ranges from 20 to 80 mg per day.
> 

> Urgent: The target dose for Lisinopril is listed as "20 mg once daily". However, the patient is already on a higher dose of "25 mg once daily". This seems to be a contradiction.
>

### Chart Data

A highly simplified version of the Chart's database is managed through a Django admin interface. It includes the following models:

- Caretakers: Doctors, Residents, Fellows, Nurses, etc.
- Patients: Patient and their care plan.
- Notes: Updates on patient care.


### The Agent

The agent has the following endpoints available to interact with (Note: port 8888 vs. 8000)

- [http://localhost:8888/observe/playground/](http://localhost:8888/observe/playground/): Reports on the latest status of the patient and any issues the agent notices about the patient.
- [http://localhost:8888/care_plan/playground/](http://localhost:8888/care_plan/playground/): Generates a new care plan on the available patient information in the chart.
- [http://localhost:8888/ask](http://localhost:8888/ask): Ask the agent a question about the patient and all other information.

### Quick setup

```bash
% cd /<your_working_dir>
% git clone https://github.com/adnantium/livechart.git
% poetry install
% source .venv/bin/activate
% export PYTHONPATH=`pwd`:`pwd`/chart/
% export DJANGO_SETTINGS_MODULE=chart.settings
% cd livechart/
% poetry install
% cd chart/
% python manage.py migrate
% django-admin loaddata demo_data.json
% python manage.py runserver
```

Go to http://localhost:8000/patient_data/1/ to see the raw text data that will be sent to the agent. It essentially contains the demo data in an LLM friendly format.


