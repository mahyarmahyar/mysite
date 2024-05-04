from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib.auth.hashers import check_password
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import CustomPasswordResetForm, CustomSetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage


def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST['username_or_email']
        password = request.POST['password']
        user = None
        if '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
                if user and check_password(password, user.password):
                    login(request, user)
                    return redirect('/')
            except User.DoesNotExist:
                pass
        else:
            user = authenticate(
                request, username=username_or_email, password=password)

            if user is not None:
                if request.user.is_authenticated:
                    return redirect('/')
                else:
                    login(request, user)
                    return redirect('/')
    else:
        if request.user.is_authenticated:
            return redirect('/')
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')

        form = CustomUserCreationForm()
        context = {'form': form}
        return render(request, 'accounts/signup.html', context)

    else:
        return redirect('/')


def forgot_password(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = 'فراموشی رمز عبور'
                    email_template_name = 'accounts/password_reset_email.html'
                    c = {
                        "email": user.email,
                        'domain': get_current_site(request).domain,
                        'site_name': 'وبسایت',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = EmailMessage(
                        subject,
                        render_to_string(email_template_name, c),
                        to=[user.email],
                    )
                    email.send()
            return redirect('password_reset_done')
    else:
        form = CustomPasswordResetForm()
    return render(request, 'accounts/password_reset_form.html', {'form': form})


def reset_password(request, uidb64, token):
    UserModel = User
    assert uidb64 is not None and token is not None  # checked by URLconf
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                return redirect('password_reset_complete')
        else:
            form = CustomSetPasswordForm()
        return render(request, 'accounts/password_reset_confirm.html', {'form': form})
    else:
        return render(request, 'accounts/password_reset_invalid.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        # انجام منطق تغییر رمز عبور در اینجا
        pass
    else:
        return render(request, 'accounts/change_password.html')
