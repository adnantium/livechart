from django.contrib import admin
from django.contrib import admin

from .models import (
    CareTaker,
    Patient,
    Note,
)

@admin.register(CareTaker)
class CareTakerAdmin(admin.ModelAdmin):
    list_display = ['name', 'role']

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'admission_datetime']

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['patient', 'creator', 'note_type', 'datetime', 'is_enabled']
