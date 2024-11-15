import threading
from django.shortcuts import render, redirect, get_object_or_404
from .forms import customUserCreationForm, custom_login, CustomPasswordChangeForm, CustomChangeProfileForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import User
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

# email configuration settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .tokens import TokenGenerator, generate_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import send_mail, EmailMessage
from django.core import mail

# custom registration form
def custom_user(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = customUserCreationForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']                    

                if first_name and last_name == 'name':
                    messages.error(request, 'please enter correct name')
                elif len(first_name) < 3:
                    messages.error(request, 'Name should be greater than 3 characters')
                else:
                    email = form.cleaned_data['email']
                    user = form.save(commit=False)
                    user.is_active = False
                    user.save()
                    
                    #sending email confirmation for activate account
                    current_site = get_current_site(request).domain
                    email_subject = "Action Required to activate your account "
                    message = render_to_string('email/activate_email.html',{
                        'user':user,
                        'domain': current_site,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': generate_token.make_token(user)
                    })
                    email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
                    EmailThread(email_message).start() # for better experience sending mails 
                    #end email confirmation
                    messages.success(request, 'You need to confirm your email address. Please check your email.!')
                    return redirect('login')
        else:
            form = customUserCreationForm()
        return render(request, 'user/user_register.html', {'form': form})
    else:
        return redirect('todo_list')


# custom login form
def custom_login_view(request):

    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = custom_login(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']

                # Check if the email exists
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    messages.error(request, "Email doesn't exist")
                    return redirect('login')

                # Check if the provided password is correct
                if user.check_password(password):
                    user = authenticate(
                        request, email=email, password=password)
                    if user is not None:
                        login(request, user)
                        messages.success(request, 'Logged in successfully.')
                        return redirect('todo_list')
                    else:
                        messages.error(
                            request, 'You need to account your account. please check your email')
                else:
                    messages.error(request, 'incorrect password')
        else:
            form = custom_login()
        context = {'form': form}
        return render(request, 'user/login.html', context)
    return redirect('todo_list')


# user logout view
def logout_user(request):
    logout(request)
    return redirect('todo_list')


# user profile
@login_required
def user_profile_view(request):
    if request.user.is_authenticated:
        user = request.user
        last_login_utc = user.last_login
        date_joined_utc = user.date_joined        
        time_difference = timedelta(hours=5, minutes=30)
        last_login_local = last_login_utc + time_difference
        date_joined_local = date_joined_utc + time_difference

        context = {'user': user, 'last_login': last_login_local, 'date_joined':date_joined_local}
        return render(request, 'user/profile_view.html', context)
    else:
        return redirect('login')


# activating user account through email
def account_activate(request, uidb64, token ):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = uid)
    except:
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        # sending an email for successfully activated account
        message = "You are successfully activated your account. Thank you!"
        subject = 'Congratulations!'
        send_mail(
			subject,
			message,
			settings.EMAIL_HOST_USER,
			[user.email],
			fail_silently = False
			)
        return render(request, 'email/email_confirm.html')
    return render(request, 'email/activation_failed.html')


# updating user profile view
@login_required
def update_user_profile(request):
    user = get_object_or_404(User, pk=request.user.id)
    form = CustomChangeProfileForm(instance=user)

    if request.method == "POST":
        form = CustomChangeProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('todo_list')
        else:
            # Handle the case when the form is not valid
            messages.error(
                request, 'Error updating profile. Please check the form.')

    context = {'form': form, 'user': user}
    return render(request, "user/update_user_profile.html", context)


# user change password / update password
@login_required
def password_change(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                old_password = request.POST['old_password']
                new_password1 = request.POST['new_password1']
                new_password2 = request.POST['new_password2']
                
                if new_password1 != new_password2:
                    messages.warning(request, "Your passwords didn't match")
                    return render(request, 'user/update_password.html', {'form': form})
                
                if old_password == new_password2:
                    messages.warning(request, 'This password is similar to your old password!')
                    return render(request, 'user/update_password.html', {'form': form})

                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Password updated successfully')
                return redirect('todo_list')
        else:
            form = CustomPasswordChangeForm(user=request.user)
        return render(request, 'user/update_password.html', {'form': form})

    else:
        return redirect('login')


# email threading used for sending emails without delay
class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        return self.email_message.send()


# user reset password / forgot password
def request_reset_password(request):
    if request.method == "POST":
        email = request.POST['email']
        user = User.objects.filter(email=email)

        if user.exists():
            current_site = get_current_site(request)
            email_subject = 'Request Reset password'
            message = render_to_string('email/reset_password.html', {
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0])
            })
            email_message = EmailMessage(
                email_subject, message, settings.EMAIL_HOST_USER, [email])
            EmailThread(email_message).start()
            messages.info(request, 'email send successfully!')
            return render(request, 'email/reset_user_password.html')
        else:
            messages.error(
                request, 'email does not exist!. Please enter correct email address.')
            return render(request, 'email/reset_user_password.html')
    else:
        return render(request, 'email/reset_user_password.html')


# setting new password 
def set_new_password(request, uidb64, token):
    context = {'uidb64': uidb64, 'token': token, }
    if request.method == 'POST':
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        if password != confirm_password:
            messages.warning(request, "password didn't match")
            return render(request, 'email/set_new_password.html', context)

        if len(password) <= 7:
            messages.warning(request, 'password must be 8 characters or above')
            return render(request, 'email/set_new_password.html', context)

        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
        if user.check_password(password):
            messages.warning(request, 'This password is similar to your old password!')
            return render(request, 'email/set_new_password.html', context)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, 'password resetted successfully.')
            return redirect('login')
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, 'Something went wrong!!!')
            return render(request, 'email/set_new_password.html', context)
    try:
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)

        if not PasswordResetTokenGenerator().check_token(user, token):
            messages.warning(request, "Password link is invalid.!!!")
            return redirect('request_reset_password')
    except DjangoUnicodeDecodeError as identifier:
        pass

    return render(request, 'email/set_new_password.html', context)
