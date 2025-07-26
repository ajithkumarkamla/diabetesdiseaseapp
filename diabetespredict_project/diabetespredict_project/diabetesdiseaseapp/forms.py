from django import forms
from .models import LoginUser, DiabetesRecord,GlucoseReading


class LoginForm(forms.ModelForm):
    class Meta:
        model = LoginUser
        fields = '__all__'


class DiabetesForm(forms.ModelForm):
    pregnancies = forms.IntegerField(
        min_value=0,
        max_value=20,
        required=True,
        label="Pregnancies",
        widget=forms.NumberInput(attrs={
            'placeholder': 'values must be 0–20'
        })
    )
    glucose = forms.FloatField(
        min_value=0,
        max_value=300,
        required=True,
        label="Glucose Level",
        widget=forms.NumberInput(attrs={
            'step': 'any',
            'placeholder': 'values must be 0–300'
        })
    )
    blood_pressure = forms.FloatField(
        min_value=0,
        max_value=200,
        required=True,
        label="Blood Pressure",
        widget=forms.NumberInput(attrs={
            'step': 'any',
            'placeholder': 'values must be 0–200'
        })
    )
    skin_thickness = forms.FloatField(
        min_value=0,
        max_value=100,
        required=True,
        label="Skin Thickness",
        widget=forms.NumberInput(attrs={
            'step': 'any',
            'placeholder': 'values must be 0–100'
        })
    )
    insulin = forms.FloatField(
        min_value=0,
        max_value=900,
        required=True,
        label="Insulin Level",
        widget=forms.NumberInput(attrs={
            'step': 'any',
            'placeholder': 'values must be 0–900'
        })
    )
    bmi = forms.FloatField(
        min_value=10,
        max_value=70,
        required=True,
        label="BMI",
        widget=forms.NumberInput(attrs={
            'step': 'any',
            'placeholder': 'values must be 10–70'
        })
    )
    diabetes_pedigree_function = forms.FloatField(
        min_value=0.0,
        max_value=2.5,
        required=True,
        label="Diabetes Pedigree Function",
        widget=forms.NumberInput(attrs={
            'step': 'any',
            'placeholder': 'values must be 0.0–2.5'
        })
    )
    age = forms.IntegerField(
        min_value=1,
        max_value=120,
        required=True,
        label="Age",
        widget=forms.NumberInput(attrs={
            'placeholder': 'values must be 1–120'
        })
    )

    class Meta:
        model = DiabetesRecord
        exclude = ['user', 'result', 'created_at', 'prediction_result']

class GlucoseReadingForm(forms.ModelForm):
    class Meta:
        model = GlucoseReading
        fields = ['test_type', 'glucose_level', 'mood']
        widgets = {
            'test_type': forms.Select(attrs={'class': 'form-control'}),
            'glucose_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'mood': forms.Select(attrs={'class': 'form-control'}),
        }
