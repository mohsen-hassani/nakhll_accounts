from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from accounts.models import VerificationCode, Profile
from accounts.forms import GetPhoneForm, CodeVerificationForm, PasswordForm
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth import update_session_auth_hash


# Create your views here.

GET_PHONE = 'get_phone.html'
REGISTER = 'register.html'
LOGIN_CODE = 'login_code.html'
PASSWORD = 'password.html'
SET_PASSWORD = 'set_password.html'
CHANGE_PASSWORD = 'change_password.html'

def get_phone(request):
    '''Get phone number, register if not exist and login for already exist phones'''
    if request.method == 'POST':
        form = GetPhoneForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get('phone_number')
            request.session['phone'] = phone
            profile = Profile.objects.filter(phone_number=phone).first()
            if profile:
                return redirect('accounts_password') if profile.user.password else redirect('accounts_login_by_code')
            else:
                return redirect('accounts_register')
    return render(request, GET_PHONE)

def register(request):
    '''Register verified user with phone number '''
    phone = request.session.get('phone')
    if not phone: # User directly enter register url and no phone entered
        return redirect('accounts_get_phone')

    user = Profile.objects.filter(phone_number=phone).first()
    if user: # This user already exists, so redirect to login page
        return redirect('accounts_forget_password')

    if request.method == 'POST':
        form = CodeVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('verification_code')
            verified = VerificationCode.verificaiton.verify_code(phone, code)
            if verified:
                # Create and login user to dashboard
                user = User.objects.create(username=phone)
                login(request, user)
                return redirect('accounts_dashboard')
            else:
                form.add_error(None, _('کد تایید شما اشتباه است یا زمان آن منقضی شده است'))
    else:
        form = CodeVerificationForm()
    code, expire_datetime = VerificationCode.verificaiton.generate_verification_code(phone)
    data = {
        'phone': phone,
        'code': code,
        'expire_datetime': expire_datetime,
        'form': form,
    }
    return render(request, REGISTER, data)

def forget_password(request):
    '''Validate user phone number and redirect to set password'''
    phone = request.session.get('phone')
    if not phone: # User directly enter this url and no phone entered
        return redirect('accounts_get_phone')
    profile = Profile.objects.filter(phone_number=phone).first()
    if not profile: # This user not exists, so redirect to register page
        return redirect('accounts_register')

    if request.method == 'POST':
        form = CodeVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('verification_code')
            verified = VerificationCode.verificaiton.verify_code(phone, code)
            if verified:
                # Login user, clear last password and redirect to set new password
                profile.user.password = ''
                profile.user.save()
                login(request, profile.user)
                return redirect('accounts_set_password')
            else:
                form.add_error(None, _('کد تایید شما اشتباه است یا زمان آن منقضی شده است'))
    else:
        form = CodeVerificationForm()
    code, expire_datetime = VerificationCode.verificaiton.generate_verification_code(phone)
    data = {
        'phone': phone,
        'code': code,
        'expire_datetime': expire_datetime,
        'form': form,
    }
    return render(request, LOGIN_CODE, data)


@login_required
def change_password(request):
    '''Change password for logged in uesrs '''
    user = request.user
    if not user.password: # User not set password yet, redirect to set password form
        return redirect('accounts_set_password')
    
    if request.method == 'POST':
        form = PasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts_dashboard')
    else:
        form = PasswordChangeForm(user=user)
    data = {
        'form': form,
    }
    return render(request, CHANGE_PASSWORD, data)



@login_required
def set_password(request):
    '''Set password for logged in uesrs '''
    user = request.user
    if user.password: # User already set password, so redirect to change password form
        return redirect('accounts_change_password')
    
    if request.method == 'POST':
        form = SetPasswordForm(user=user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts_dashboard')
    else:
        form = SetPasswordForm(user=user)
    data = {
        'form': form,
    }
    return render(request, SET_PASSWORD, data)

def password(request):
    '''Authenticate user with phone as username and password '''
    phone = request.session.get('phone')
    if not phone: # User directly enter this url and no phone entered
        return redirect('accounts_get_phone')
    profile = Profile.objects.filter(phone_number=phone).first()
    if not profile: # This user not exists, so redirect to register page
        return redirect('accounts_register')
    if not profile.user.password: # User not set password yet, redirect to login by code
        return redirect('accounts_login_by_code')

    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password', '')
            user = authenticate(username=phone, password=password)
            if user:
                login(request, user)
                return redirect('accounts_dashboard')
            else:
                form.add_error(None, _('رمز ورود شما اشتباه است'))
    else:
        form = PasswordForm()
    data = {
        'form': form,
        'phone': phone,
    }
    return render(request, PASSWORD, data)


def login_by_code(request):
    '''Send a code to user phone and verify to login '''
    phone = request.session.get('phone')
    if not phone: # User directly enter this url and no phone entered
        return redirect('accounts_get_phone')
    profile = Profile.objects.filter(phone_number=phone).first()
    if not profile: # This user not exists, so redirect to register page
        return redirect('accounts_register')

    if request.method == 'POST':
        form = CodeVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('verification_code')
            verified = VerificationCode.verificaiton.verify_code(phone, code)
            if verified:
                # Login user
                login(request, profile.user)
                return redirect('accounts_dashboard')
            else:
                form.add_error(None, _('کد تایید شما اشتباه است یا زمان آن منقضی شده است'))
    else:
        form = CodeVerificationForm()
    code, expire_datetime = VerificationCode.verificaiton.generate_verification_code(phone)
    data = {
        'phone': phone,
        'code': code,
        'expire_datetime': expire_datetime,
        'form': form,
    }
    return render(request, LOGIN_CODE, data)


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('accounts_get_phone')