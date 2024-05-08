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
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from .forms import LoginForm
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.urls import reverse


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
        print(request.method)
        print(request.POST)
        # Process the form submission
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
                    reset_url = reverse('accounts:reset_password', kwargs={
                                        'uidb64': uid, 'token': token})

                    # Send reset password email
                    subject = 'Password Reset'
                    email_template_name = 'accounts/password_reset_email.html'
                    c = {
                        "email": user.email,
                        'domain': get_current_site(request).domain,
                        "uid": uid,
                        "user": user,
                        'token': token,
                        'reset_url': reset_url,
                        'protocol': 'http',
                    }
                    email_content = render_to_string(email_template_name, c)
                    send_mail(subject, email_content,
                              'admin@example.com', [user.email])

                # Show success message to the user
                messages.success(
                    request, 'An email has been sent to reset your password. Please check your inbox.')

                # Redirect to the login page
                return redirect('accounts:login')
            else:
                messages.error(
                    request, 'No user found with this email address.')
    else:
        form = CustomPasswordResetForm()

    return render(request, 'accounts/password_reset_form.html', {'form': form})


def reset_password(request, uidb64, token):
    if request.method == 'POST':
        form = CustomSetPasswordForm(request.user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password2']
            uid = urlsafe_base64_decode(uidb64).decode('utf-8')
            user = User.objects.get(pk=uid)
            user.set_password(new_password)
            user.save()
            return redirect('password_reset_complete')
    else:
        form = CustomSetPasswordForm()
    return render(request, 'accounts/password_reset_confirm.html', {'form': form})
