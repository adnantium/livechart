from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"

class Resident(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.name}"

class Patient(models.Model):
    name = models.CharField(max_length=100)
    brief_description = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.name}"

class DoctorNote(models.Model):
    """
    Represents a note written by a doctor for a patient.

    Attributes:
        doctor (Doctor): The doctor who wrote the note.
        patient (Patient): The patient for whom the note is written.
        text (str): The content of the note.
        priority (str): The priority level of the note.
        datetime (datetime): The date and time when the note was created.
    """
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    text = models.TextField()
    priority = models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])
    datetime = models.DateTimeField(auto_created=True, auto_now=True)

class ResidentNote(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    text = models.TextField()
    datetime = models.DateTimeField(auto_created=True, auto_now=True)

class AINote(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    text = models.TextField()
    datetime = models.DateTimeField(auto_created=True, auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.patient} - {self.datetime}"

class LabResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    text = models.TextField()
    datetime = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self) -> str:
        return f"{self.patient} - {self.datetime}"


class CarePlan(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    text = models.TextField()
    datetime = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self) -> str:
        return f"{self.patient} - {self.datetime}"

class GeneratedCarePlan(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    text = models.TextField()
    datetime = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self) -> str:
        return f"{self.patient} - {self.datetime}"
