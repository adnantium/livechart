from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.template.loader import render_to_string

from .models import Patient

       
def patient_data(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    template_context = {
        'patient': patient,
        'notes': patient.note_set.all(),
    }
    rendered = render_to_string('patient_data.txt', template_context)
    return HttpResponse(rendered, content_type='text/plain')

    # patient_json = serializers.serialize('json', [patient])
    # return JsonResponse(patient_json, safe=False)
    # return HttpResponse(patient_json, content_type='application/json')

