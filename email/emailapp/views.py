from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import EmailReply
from .forms import EmailReplyForm
# =========================
# REGISTER
# =========================
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()
        messages.success(request, "Registration Successful")
        return redirect('login')
    return render(request, 'register.html')
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
def landing(request):
    return render(request, 'landing.html')
@csrf_exempt
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        return JsonResponse({
            "message": "User registered successfully"
        })
# ========================
# LOGIN
# =========================
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect('login')
    return render(request, 'login.html')
# =========================
# LOGOUT
# =========================
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
# =========================
# DASHBOARD
# =========================
@login_required
def dashboard(request):
    total_replies = EmailReply.objects.filter(
        user=request.user
    ).count()
    return render(request, 'dashboard.html', {
        'total_replies': total_replies
    })
# =========================
# CREATE
# =========================
@login_required
def create_reply(request):
    if request.method == 'POST':
        form = EmailReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.save()
            messages.success(request, "Reply Saved Successfully")
            return redirect('history')
    else:
        form = EmailReplyForm()
    return render(request, 'create.html', {
        'form': form
    })
# =========================
# READ / HISTORY
# =========================
@login_required
def history(request):
    replies = EmailReply.objects.filter(
        user=request.user
    ).order_by('-created_at')
    return render(request, 'history.html', {
        'replies': replies
    })
# =========================
# UPDATE
# =========================
@login_required
def update_reply(request, id):
    reply = get_object_or_404(
        EmailReply,
        id=id,
        user=request.user
    )
    if request.method == 'POST':
        form = EmailReplyForm(
            request.POST,
            instance=reply
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Reply Updated Successfully")
            return redirect('history')
    else:
        form = EmailReplyForm(instance=reply)
    return render(request, 'update.html', {
        'form': form
    })
# =========================
# DELETE
# =========================
@login_required
def delete_reply(request, id):
    reply = get_object_or_404(
        EmailReply,
        id=id,
        user=request.user
    )
    if request.method == 'POST':
        reply.delete()
        messages.success(request, "Reply Deleted Successfully")
        return redirect('history')
    return render(request, 'delete.html', {
        'reply': reply
    })
    
    
    
    
    
    
    
    
    
    

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# ==========================================
# AI EMAIL GENERATOR API
# ==========================================
@csrf_exempt
def generate_email_reply(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            tone = data.get("tone", "Professional")
            # LONG FORMAT AI EMAIL REPLY
            reply = f"""
Dear Sir/Madam,
Thank you for reaching out and sharing your email with us.
I appreciate the time and effort you took to explain the matter clearly. After carefully reviewing your message, I would like to respond in a {tone.lower()} manner.
Regarding your email:
\"{email}\"
I completely understand the importance of this situation and I truly value your communication. Please be assured that your message has been reviewed properly and necessary attention will be given to the matter discussed.
If any additional clarification, information, or support is required from my side, please feel free to let me know. I would be happy to assist further and ensure smooth communication moving forward.
Thank you once again for your patience, understanding, and cooperation. I look forward to staying connected and working together effectively.
Best Regards,
AI Email Reply Generator
Customer Support Team
"""
            return JsonResponse({
                "reply": reply
            })
        except Exception as e:
            return JsonResponse({
                "error": str(e)
            })
    return JsonResponse({
        "error": "Invalid request method"
    })
# ==========================================
# DASHBOARD VIEW
# ==========================================
def dashboard(request):
    reply = ""
    if request.method == "POST":
        email_content = request.POST.get("email")
        tone = request.POST.get("tone")
        # LONG FORMAT AI REPLY
        reply = f"""
Dear Sir/Madam,
Thank you for your email.
I appreciate you contacting us regarding the following matter:
\"{email_content}\"
After reviewing your message carefully, I would like to provide a {tone.lower()} response.
Your email has been received successfully, and I truly understand the importance of your concern. Please be assured that the matter will be handled with proper attention and professionalism.
We always value clear communication and maintaining a positive relationship with our clients, customers, and team members. If there are any updates, additional details, or further requirements, please do not hesitate to contact us.
Thank you once again for your patience and understanding. I look forward to assisting you further.
Best Regards,
AI Email Reply Generator
Support Department
"""
    context = {
        "reply": reply
    }
    return render(
        request,
        "dashboard.html",
        context
    )