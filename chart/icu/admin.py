from django.contrib import admin
from django.contrib import admin

from .models import (
    Doctor,
    Resident,
    Patient,
    DoctorNote,
    ResidentNote,
    LabResult,
    CarePlan,
    GeneratedCarePlan,
    AINote
)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'speciality', ]

@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', ]

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'brief_description', ]

@admin.register(DoctorNote)
class DoctorNoteAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'patient', 'text', 'priority', 'datetime',]

@admin.register(ResidentNote)
class ResidentNoteAdmin(admin.ModelAdmin):
    list_display = ['resident', 'patient', 'text', 'datetime',]

@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = ['patient', 'text', 'datetime', ]

@admin.register(CarePlan)
class CarePlanAdmin(admin.ModelAdmin):
    list_display = ['patient', 'text', 'datetime', ]


@admin.register(GeneratedCarePlan)
class GeneratedCarePlanAdmin(admin.ModelAdmin):
    list_display = ['patient', 'text', 'datetime', ]
    
@admin.register(AINote)
class AINoteAdmin(admin.ModelAdmin):
    list_display = ['patient', 'text', 'datetime', ]