from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_control
import datetime
from .models import Patient


@cache_control(private=True)
def patient_data(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    template_context = {
        "patient": patient,
        "notes": patient.note_set.filter(is_enabled=True).order_by("datetime"),
        "current_datetime": datetime.datetime.now(),
    }
    rendered = render_to_string("patient_data.txt", template_context)
    return HttpResponse(rendered, content_type="text/plain")
