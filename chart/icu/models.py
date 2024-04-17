from django.db import models



class CareTaker(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, choices=[
        ("doctor", "Doctor"),
        ("resident", "Resident"),
        ("livechart", "Live Chart"),
    ])
    
    def __str__(self) -> str:
        return f"{self.name} ({self.role})"

class Patient(models.Model):
    name = models.CharField(max_length=255)
    admission_datetime = models.DateTimeField()
    care_plan = models.TextField()
    
    def __str__(self) -> str:
        return f"{self.name} ({self.admission_datetime})"

class Note(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    creator = models.ForeignKey(CareTaker, on_delete=models.CASCADE)
    note_type = models.CharField(max_length=255, choices=[
        ("doctor", "Doctor"),
        ("resident", "Resident"),
        ("lab_result", "Lab Result"),
        ("care_plan", "Care Plan"),
        ("generated_care_plan", "AI Generated Care Plan"),
    ])
    datetime = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    is_enabled = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.patient} - {self.note_type} ({self.datetime})"

