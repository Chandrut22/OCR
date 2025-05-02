import os
import json
import random
import asyncio
import smtplib
from textblob import TextBlob
from datetime import timedelta
from .models import CustomUser 
from dotenv import load_dotenv
from googletrans import Translator
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from email.mime.text import MIMEText
from django.utils.timezone import now
from pydantic_ai import Agent, BinaryContent
from django.shortcuts import render, redirect
from email.mime.multipart import MIMEMultipart
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, JsonResponse
from django.contrib.auth import authenticate, login, logout


load_dotenv()

def read_image(file_path):
    try:
        with open(file_path, "rb") as file:
            return file.read()
    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"Error reading file: {str(e)}"
    
def logout_view(request):
    logout(request)
    return redirect('index')

def index(request):
    full_name = request.user.name if request.user.is_authenticated else ""
    return render(request, "index.html", {'full_name': full_name})

def generate_verification_code():
    return str(random.randint(100000, 999999))

def forgot_password(request):
    return render(request, 'forgot_password.html')




@csrf_exempt
def send_verification_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)

            verification_code = generate_verification_code()
            user.verification_code = verification_code
            user.code_expiry = now() + timedelta(minutes=10)  
            user.save()

            template_path = os.path.join(settings.BASE_DIR, 'web', 'templates', 'verification_email.html')
            with open(template_path, 'r') as file:
                html_template = file.read()
            
            html_content = html_template.replace('{verification_code}', verification_code)

            subject = "Your OCR App Verification Code"
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = settings.EMAIL_HOST_USER
            msg['To'] = email

            text_content = f"Your verification code is: {verification_code}. This code will expire in 10 minutes."
            part1 = MIMEText(text_content, 'plain')
            part2 = MIMEText(html_content, 'html')
            
            msg.attach(part1)
            msg.attach(part2)

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, email, msg.as_string())
            server.quit()

            return JsonResponse({'message': 'Verification code sent successfully'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Email not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def verify_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code = request.POST.get('code')
        try:
            user = CustomUser.objects.get(email=email)
            if user.verification_code == code and user.code_expiry > now():
                return JsonResponse({'message': 'Code verified successfully'})
            else:
                return JsonResponse({'error': 'Invalid or expired code'}, status=400)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)


@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        try:
            user = CustomUser.objects.get(email=email)
            user.set_password(new_password)
            user.verification_code = ""
            user.code_expiry = None
            user.save()
            return JsonResponse({'message': 'Password reset successful'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)


@csrf_exempt
def translate_text(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text')
        language = data.get('language')

        async def translate(text, language):
            translator = Translator()
            translation = await translator.translate(text, dest=language)
            return translation

        try:
            translation = asyncio.run(translate(text, language))
            return JsonResponse({
                'translated_text': translation.text,
                'language': translation.dest
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def spell_check(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text')
        blob = TextBlob(text)
        corrected_text = blob.correct()
        
        return JsonResponse({
            'original_text': text,
            'corrected_text': str(corrected_text)
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required(login_url='login')
def upload(request):
    full_name = request.user.name if request.user.is_authenticated else ""
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name
        file_path = os.path.join(settings.MEDIA_ROOT, "uploads", file_name)

        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        request.session['uploaded_file'] = file_name

        return redirect('output', file_name=file_name)

    return render(request, "upload.html", {'full_name': full_name})



@login_required(login_url='login')
def output(request, file_name):
    full_name = request.user.name if request.user.is_authenticated else ""
    file_path = os.path.join(settings.MEDIA_ROOT, "uploads", file_name)

    if not os.path.exists(file_path):
        return HttpResponseNotFound("File not found.")

    image_data = read_image(file_path)

    if isinstance(image_data, str):  
        return image_data

    try:
        agent = Agent(model='google-gla:gemini-2.0-flash-lite')
        result = agent.run_sync(
            [
                "extract the text in the image and provide only the text.",
                BinaryContent(data=image_data, media_type="image/png"),  
            ]
        )
        file_url = os.path.join(settings.MEDIA_URL, "uploads", file_name)
        return render(request, "output.html", {
            'full_name': full_name,
            'extracted_text': result.data,
            'file_url': file_url,
            'lang': lang
        })
    except Exception as e:
        return HttpResponseNotFound(str(e))

@login_required(login_url='login')
def delete_uploaded_file(request):
    if request.method == 'POST':
        file_name = request.session.get('uploaded_file')
        if file_name:
            file_path = os.path.join(settings.MEDIA_ROOT, "uploads", file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
                del request.session['uploaded_file']  
                return JsonResponse({'message': 'File deleted successfully.'})
        return JsonResponse({'error': 'No file to delete.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(email=email)  
        except CustomUser.DoesNotExist:
            messages.error(request, 'No account found with that email address.')
            return render(request, 'login.html')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            full_name = user.name  
            return redirect('index') 
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'login.html')

def signup_view(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'login.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'login.html')

        user = CustomUser.objects.create_user(email=email, name=name, password=password)
        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('login')

    return render(request, 'login.html')

lang = {
    'bn': 'Bengali',
    'zh-cn': 'Chinese (simplified)',
    'zh-tw': 'Chinese (traditional)',
    'en': 'English',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'hi': 'Hindi',
    'ja': 'Japanese',
    'kn': 'Kannada',
    'la': 'Latin',
    'ml': 'Malayalam',
    'ne': 'Nepali',
    'or': 'Odia',
    'pt': 'Portuguese',
    'pa': 'Punjabi',
    'ru': 'Russian',
    'es': 'Spanish',
    'ta': 'Tamil',
    'te': 'Telugu',
    'th': 'Thai',
    'ur': 'Urdu',
}