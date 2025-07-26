from django.db import models
from django.contrib.auth.models import User

class LoginUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

class DiabetesRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    pregnancies = models.PositiveIntegerField()
    glucose = models.FloatField()
    blood_pressure = models.FloatField()
    skin_thickness = models.FloatField()
    insulin = models.FloatField()
    bmi = models.FloatField()
    diabetes_pedigree_function = models.FloatField()
    age = models.PositiveIntegerField()

    prediction_result = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.prediction_result}"

class GlucoseReading(models.Model):
    TEST_TYPE_CHOICES = [
        ('Fasting', 'Fasting'),
        ('Postprandial', 'Postprandial'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_type = models.CharField(max_length=20, choices=TEST_TYPE_CHOICES)
    glucose_level = models.FloatField()
    mood = models.CharField(
        max_length=10,
        choices=[('good', '😊 Good'), ('okay', '😐 Okay'), ('tired', '😞 Tired')],
        blank=True,
        null=True
    )
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.test_type} - {self.glucose_level}"


