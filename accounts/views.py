from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import UserProfile


def _login_user(request, profile):
    request.session['user_id'] = profile.pk
    request.session['user_name'] = profile.name or profile.email
    request.session['user_email'] = profile.email


def signup_view(request):
    context = {
        'form': {},
        'error': None,
    }

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        age = request.POST.get('age', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')

        context['form'] = {
            'name': name,
            'age': age,
            'email': email,
        }

        if not name or not age or not email or not password or not password_confirm:
            context['error'] = 'Please complete all fields.'
        elif not age.isdigit() or int(age) < 13:
            context['error'] = 'Please enter a valid age (13+).'
        elif password != password_confirm:
            context['error'] = 'Passwords do not match.'
        elif len(password) < 8:
            context['error'] = 'Password must be at least 8 characters.'
        elif UserProfile.objects.filter(email=email).exists():
            context['error'] = 'An account with this email already exists.'
        else:
            profile = UserProfile.objects.create(
                name=name,
                age=int(age),
                email=email,
                password=make_password(password),
            )
            _login_user(request, profile)
            return redirect(reverse('career:chat'))

    return render(request, 'accounts/signup.html', context)


def signin_view(request):
    context = {
        'form': {},
        'error': None,
    }

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        context['form'] = {'email': email}

        try:
            profile = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            profile = None

        if not profile or not password:
            context['error'] = 'Invalid email or password.'
        elif not profile.password or not check_password(password, profile.password):
            context['error'] = 'Invalid email or password.'
        else:
            _login_user(request, profile)
            if profile.interest_text:
                return redirect(reverse('career:roadmap'))
            return redirect(reverse('career:chat'))

    return render(request, 'accounts/signin.html', context)


def logout_view(request):
    request.session.flush()
    return redirect(reverse('how-it-works'))
