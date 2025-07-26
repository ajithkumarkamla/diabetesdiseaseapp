from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .forms import DiabetesForm,GlucoseReadingForm
from .models import DiabetesRecord,GlucoseReading
import pickle
import os
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.contrib.auth import logout

# Load the machine learning model
def load_model():
    model_path = os.path.join(settings.BASE_DIR, 'diabetes_model.pkl')
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    return model

# Use load_model() to get the trained model
model = load_model()


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def index(request):
    return render(request, 'index.html')


@login_required
def predict(request):
    form = DiabetesForm()
    return render(request, 'predict.html', {'form': form})

def get_health_tips(prediction):
    if prediction == 1:
        return [
            "Maintain a balanced, low-sugar diet.",
            "Exercise regularly (at least 30 minutes/day).",
            "Monitor your blood sugar levels regularly.",
            "Avoid sugary drinks and processed foods.",
            "Consult your doctor for personalized medication."
        ]
    else:
        return [
            "Continue eating a healthy, balanced diet.",
            "Stay physically active.",
            "Maintain a healthy weight.",
            "Prioritize getting quality sleep every night.",
            "Go for regular health check-ups."
        ]

def result(request):
    if request.method == 'POST':
        form = DiabetesForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            values = [
                cd['pregnancies'], cd['glucose'], cd['blood_pressure'],
                cd['skin_thickness'], cd['insulin'], cd['bmi'],
                cd['diabetes_pedigree_function'], cd['age']
            ]

            # 🔮 Get prediction and probability
            prediction = model.predict([values])[0]
            probabilities = model.predict_proba([values])
            confidence_score = round(probabilities[0][prediction] * 100, 2)  # in percentage

            # 🧠 Determine result message
            result_text = "You have diabetes." if prediction == 1 else "You don't have diabetes."

            # ⚠️ Optional: Add risk level
            if confidence_score >= 80:
                risk = "High Risk"
            elif confidence_score >= 50:
                risk = "Moderate Risk"
            else:
                risk = "Low Risk"

            # 💾 Save to database if user is logged in
            record = None
            if request.user.is_authenticated:
                record = DiabetesRecord.objects.create(
                    user=request.user,
                    pregnancies=cd['pregnancies'],
                    glucose=cd['glucose'],
                    blood_pressure=cd['blood_pressure'],
                    skin_thickness=cd['skin_thickness'],
                    insulin=cd['insulin'],
                    bmi=cd['bmi'],
                    diabetes_pedigree_function=cd['diabetes_pedigree_function'],
                    age=cd['age'],
                    prediction_result=result_text
                )

            # 💡 Get health tips
            health_tips = get_health_tips(prediction)

            # 📤 Pass all values to the result page
            return render(request, 'result.html', {
                'result': result_text,
                'health_tips': health_tips,
                'record': record,
                'confidence_score': confidence_score,
                'risk': risk,
            })
        else:
            return render(request, 'predict.html', {'form': form})
    return render(request, 'predict.html', {'form': DiabetesForm()})

def contact(request):
    return render(request, 'contact.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check if any fields are empty
        if not username or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return render(request, 'register.html')

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'register.html')

        User.objects.create_user(username=username, password=password1)
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Please fill in all fields.")
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Change to your homepage URL name
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')

    return render(request, 'login.html')

@login_required
def generate_pdf(request):
    # Get the latest DiabetesRecord for the logged-in user
    try:
        record = DiabetesRecord.objects.filter(user=request.user).latest('created_at')

        # Determine the health tips based on the prediction result
        health_tips = get_health_tips(1 if "have diabetes" in record.prediction_result.lower() else 0)

        # Render the template to generate the HTML content
        template = get_template('report_template.html')
        html = template.render({
            'record': record,
            'health_tips': health_tips,
            'user': request.user,
        })

        # Create the PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="diabetes_report.pdf"'

        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse("We had some errors <pre>" + html + "</pre>")
        return response
    except DiabetesRecord.DoesNotExist:
        return HttpResponse("No record found for your user.")

@login_required
def prediction_history(request):
        records = DiabetesRecord.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'history.html', {'records': records})

@login_required
def delete_record(request, record_id):
    record = get_object_or_404(DiabetesRecord, id=record_id, user=request.user)
    if request.method == 'POST':
        record.delete()
    return redirect('prediction_history')  #


def logout_view(request):
    logout(request)  # Logout the user
    return redirect('home')  #

def diabetes_info(request):
    return render(request, 'diabetes_info.html')

@login_required
def glucose_monitoring(request):
    form = GlucoseReadingForm(request.POST or None)
    readings = GlucoseReading.objects.filter(user=request.user).order_by('-recorded_at')

    if request.method == 'POST' and form.is_valid():
        reading = form.save(commit=False)
        reading.user = request.user
        reading.save()
        return redirect('glucose_monitoring')  # redirect to same page after submission

    return render(request, 'glucose_monitoring.html', {
        'form': form,
        'readings': readings,
    })

@login_required
def delete_reading(request, reading_id):
    reading = get_object_or_404(GlucoseReading, id=reading_id, user=request.user)
    if request.method == 'POST':
        reading.delete()
        return redirect('glucose_monitoring')  # Replace with your URL name for this page
    return redirect('glucose_monitoring')