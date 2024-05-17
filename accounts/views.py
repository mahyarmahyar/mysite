from django.template import RequestContext
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomPasswordResetForm, CustomSetPasswordForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from .forms import LoginForm
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.forms import SetPasswordForm
from django.utils.encoding import force_str
from django.http import HttpResponse


def login_view(request):
    form = LoginForm(request.POST or None)  # تعریف فرم ورود
    if request.method == 'POST':
        if form.is_valid():  # بررسی اعتبار فرم
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
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
                    login(request, user)
                    return redirect('/')
            form.add_error(None, 'Invalid username or password.')
    else:
        if request.user.is_authenticated:
            return redirect('/')
    return render(request, 'accounts/login.html', {'form': form})


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
                    # Generate a token for password reset
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = default_token_generator.make_token(user)

                    # Construct the reset password link
                    reset_url = request.build_absolute_uri(reverse('accounts:reset_password', kwargs={
                        'uidb64': uid, 'token': token}))

                    # Send reset password email
                    subject = 'Password Reset'
                    email_content = f"""
                    <html>
                      <head></head>
                      <body>
                        <p>Click <a href="{reset_url}">here</a> to reset your password.</p>
                      </body>
                    </html>
                    """
                    send_mail(subject, '', 'admin@example.com',
                              [user.email], html_message=email_content)

                # Redirect to the password reset sent page
                return redirect('accounts:password_reset_done')
            else:
                messages.error(
                    request, 'No user found with this email address.')
    else:
        form = CustomPasswordResetForm()

    return render(request, 'accounts/password_reset_form.html', {'form': form})


def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Your password has been set. You may log in now.')
                return redirect('accounts:login')
        else:
            form = CustomSetPasswordForm(user)
    else:
        messages.error(
            request, 'The password reset link is invalid, possibly because it has already been used.')
        return redirect('accounts:reset_password_invalid')

    return render(request, 'accounts/password_reset_confirm.html', {'form': form})


def reset_password_invalid(request):
    return render(request, 'accounts/reset_password_invalid.html')
