from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.cache import never_cache

from django.contrib import messages
from django.contrib.auth.models import User , auth
from main_app.models import patient , doctor
from datetime import datetime, timedelta
from .forms import PatientSignupForm, DoctorSignupForm, PatientProfileUpdateForm, DoctorProfileUpdateForm
from django.conf import settings

# Create your views here.


   
def logout(request):
    """Enhanced logout with proper session cleanup and security"""
    # Get the username before logout for logging
    username = None
    user_type = None
    
    if request.user.is_authenticated:
        username = request.user.username
        if hasattr(request.user, 'patient'):
            user_type = 'patient'
        elif hasattr(request.user, 'doctor'):
            user_type = 'doctor'
        elif request.user.is_superuser:
            user_type = 'admin'
    
    # Clear all session data
    session_keys_to_remove = [
        'patientid', 'doctorid', 'adminid', 
        'patientusername', 'doctorusername', 'admin_username',
        'patient_session_start', 'doctor_session_start', 'admin_session_start'
    ]
    
    for key in session_keys_to_remove:
        request.session.pop(key, None)
    
    # Logout user
    auth.logout(request)
    
    # Add success message
    messages.success(request, 'You have been successfully logged out.')
    
    # Log the logout event (for audit purposes)
    print(f"User logout: {username} ({user_type}) at {datetime.now()}")
    
    return redirect('homepage')




@csrf_protect
@never_cache
def sign_in_admin(request):
    """Enhanced admin login with improved security and session management"""
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Validate input
        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return redirect('sign_in_admin')

        # Rate limiting check (simple implementation)
        login_attempts_key = f'admin_login_attempts_{request.META.get("REMOTE_ADDR", "unknown")}'
        attempts = request.session.get(login_attempts_key, 0)
        
        if attempts >= 5:  # Max 5 attempts
            messages.error(request, 'Too many login attempts. Please try again later.')
            return redirect('sign_in_admin')

        # Authenticate user
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # Check if user is superuser (admin)
            if user.is_superuser and user.is_staff:
                # Reset login attempts on successful login
                request.session.pop(login_attempts_key, None)
                
                # Check if account is active
                if not user.is_active:
                    messages.error(request, 'Your account has been deactivated. Please contact support.')
                    return redirect('sign_in_admin')
                
                # Login user
                auth.login(request, user)
                
                # Store enhanced admin info in session
                request.session['adminid'] = user.id
                request.session['admin_username'] = user.username
                request.session['admin_session_start'] = datetime.now().isoformat()
                request.session['admin_login_ip'] = request.META.get('REMOTE_ADDR', 'unknown')
                
                # Log successful login
                print(f"Admin login successful: {user.username} from IP: {request.META.get('REMOTE_ADDR', 'unknown')}")
                
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('admin_ui')
            else:
                # Increment failed attempts
                request.session[login_attempts_key] = attempts + 1
                messages.error(request, 'This account does not have admin privileges.')
                return redirect('sign_in_admin')
        else:
            # Increment failed attempts
            request.session[login_attempts_key] = attempts + 1
            messages.error(request, 'Invalid username or password. Please check your credentials.')
            return redirect('sign_in_admin')
    else:
        # Handle GET request - show login form
        return render(request, 'admin/signin/signin.html')



@csrf_protect
@never_cache
def signup_patient(request):
    """Professional patient signup with comprehensive validation"""
    
    if request.method == 'POST':
        form = PatientSignupForm(request.POST)
        if form.is_valid():
            try:
                # Create user
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    email=form.cleaned_data['email']
                )
                user.save()
                
                # Parse DOB
                dob_date = form.cleaned_data['dob']
                
                # Create patient profile
                patientnew = patient(
                    user=user,
                    name=form.cleaned_data['name'],
                    dob=dob_date,
                    gender=form.cleaned_data['gender'],
                    address=form.cleaned_data['address'],
                    mobile_no=form.cleaned_data['mobile_no']
                )
                patientnew.save()
                
                messages.success(request, 'Patient account created successfully! Please sign in with your credentials.')
                return redirect('sign_in_patient')
                
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}. Please try again.')
                return render(request, 'patient/signup_form/signup.html', {'form': form})
        else:
            # Form has errors, display them
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.title()}: {error}')
            return render(request, 'patient/signup_form/signup.html', {'form': form})
    
    else:
        form = PatientSignupForm()
        return render(request, 'patient/signup_form/signup.html', {'form': form})



@csrf_protect
@never_cache
def sign_in_patient(request):
    """Enhanced patient login with improved security and session management"""
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Validate input
        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return redirect('sign_in_patient')

        # Rate limiting check
        login_attempts_key = f'patient_login_attempts_{request.META.get("REMOTE_ADDR", "unknown")}'
        attempts = request.session.get(login_attempts_key, 0)
        
        if attempts >= 5:  # Max 5 attempts
            messages.error(request, 'Too many login attempts. Please try again later.')
            return redirect('sign_in_patient')

        # Authenticate user
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            try:
                if user.patient.is_patient == True:
                    # Reset login attempts on successful login
                    request.session.pop(login_attempts_key, None)
                    
                    # Check if account is active
                    if not user.is_active:
                        messages.error(request, 'Your account has been deactivated. Please contact support.')
                        return redirect('sign_in_patient')
                    
                    # Login user
                    auth.login(request, user)

                    # Store enhanced patient info in session
                    request.session['patientusername'] = user.username
                    request.session['patient_session_start'] = datetime.now().isoformat()
                    request.session['patient_login_ip'] = request.META.get('REMOTE_ADDR', 'unknown')
                    
                    # Log successful login
                    print(f"Patient login successful: {user.username} from IP: {request.META.get('REMOTE_ADDR', 'unknown')}")
                    
                    messages.success(request, f'Welcome back, {user.username}!')
                    return redirect('patient_ui')
                    
            except patient.DoesNotExist:
                # Increment failed attempts
                request.session[login_attempts_key] = attempts + 1
                messages.error(request, 'This account is not a patient account.')
                return redirect('sign_in_patient')
        else:
            # Increment failed attempts
            request.session[login_attempts_key] = attempts + 1
            messages.error(request, 'Invalid username or password. Please check your credentials.')
            return redirect('sign_in_patient')
    else:
        return render(request, 'patient/signin_page/index.html')


def savepdata(request, patientusername):
    """Professional patient profile update with validation"""
    
    if request.method == 'POST':
        puser = User.objects.get(username=patientusername)
        patient_profile = puser.patient
        
        form = PatientProfileUpdateForm(request.POST)
        if form.is_valid():
            try:
                # Parse DOB
                dob_date = form.cleaned_data['dob']
                
                # Update patient profile
                patient.objects.filter(pk=puser.patient).update(
                    name=form.cleaned_data['name'],
                    dob=dob_date,
                    gender=form.cleaned_data['gender'],
                    address=form.cleaned_data['address'],
                    mobile_no=form.cleaned_data['mobile_no']
                )
                
                messages.success(request, 'Profile updated successfully!')
                return redirect('pviewprofile', patientusername)
                
            except Exception as e:
                messages.error(request, f'Error updating profile: {str(e)}. Please try again.')
                return redirect('pviewprofile', patientusername)
        else:
            # Form has errors, display them
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.title()}: {error}')
            return redirect('pviewprofile', patientusername)
    else:
        return redirect('pviewprofile', patientusername)





#doctors account...........operations......
    

@csrf_protect
@never_cache
def signup_doctor(request):
    """Professional doctor signup with comprehensive validation"""
    
    if request.method == 'GET':
        form = DoctorSignupForm()
        return render(request, 'doctor/signup_form/signup.html', {'form': form})

    if request.method == 'POST':
        form = DoctorSignupForm(request.POST)
        if form.is_valid():
            try:
                # Create user
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    email=form.cleaned_data['email']
                )
                user.save()
                
                # Parse dates
                dob_date = form.cleaned_data['dob']
                yor_date = form.cleaned_data['year_of_registration']
                
                # Create doctor profile
                doctornew = doctor(
                    user=user,
                    name=form.cleaned_data['name'],
                    dob=dob_date,
                    gender=form.cleaned_data['gender'],
                    address=form.cleaned_data['address'],
                    mobile_no=form.cleaned_data['mobile_no'],
                    registration_no=form.cleaned_data['registration_no'],
                    year_of_registration=yor_date,
                    qualification=form.cleaned_data['qualification'],
                    State_Medical_Council=form.cleaned_data['State_Medical_Council'],
                    specialization=form.cleaned_data['specialization']
                )
                doctornew.save()
                
                messages.success(request, 'Doctor account created successfully! Please sign in with your credentials.')
                return redirect('sign_in_doctor')
                
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}. Please try again.')
                return render(request, 'doctor/signup_form/signup.html', {'form': form})
        else:
            # Form has errors, display them
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.title()}: {error}')
            return render(request, 'doctor/signup_form/signup.html', {'form': form})








@csrf_protect
@never_cache
def sign_in_doctor(request):
    """Enhanced doctor login with improved security and session management"""
    
    if request.method == 'GET':
        return render(request, 'doctor/signin_page/index.html')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Validate input
        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return redirect('sign_in_doctor')

        # Rate limiting check
        login_attempts_key = f'doctor_login_attempts_{request.META.get("REMOTE_ADDR", "unknown")}'
        attempts = request.session.get(login_attempts_key, 0)
        
        if attempts >= 5:  # Max 5 attempts
            messages.error(request, 'Too many login attempts. Please try again later.')
            return redirect('sign_in_doctor')

        # Authenticate user
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            try:
                if user.doctor.is_doctor == True:
                    # Reset login attempts on successful login
                    request.session.pop(login_attempts_key, None)
                    
                    # Check if account is active
                    if not user.is_active:
                        messages.error(request, 'Your account has been deactivated. Please contact support.')
                        return redirect('sign_in_doctor')
                    
                    # Login user
                    auth.login(request, user)
                    
                    # Store enhanced doctor info in session
                    request.session['doctorusername'] = user.username
                    request.session['doctor_session_start'] = datetime.now().isoformat()
                    request.session['doctor_login_ip'] = request.META.get('REMOTE_ADDR', 'unknown')
                    
                    # Log successful login
                    print(f"Doctor login successful: {user.username} from IP: {request.META.get('REMOTE_ADDR', 'unknown')}")
                    
                    messages.success(request, f'Welcome back, Dr. {user.username}!')
                    return redirect('doctor_ui')
                    
            except doctor.DoesNotExist:
                # Increment failed attempts
                request.session[login_attempts_key] = attempts + 1
                messages.error(request, 'This account is not a doctor account.')
                return redirect('sign_in_doctor')
        else:
            # Increment failed attempts
            request.session[login_attempts_key] = attempts + 1
            messages.error(request, 'Invalid username or password. Please check your credentials.')
            return redirect('sign_in_doctor')
    else:
        return render(request, 'doctor/signin_page/index.html')





def saveddata(request, doctorusername):
    """Professional doctor profile update with validation"""
    
    if request.method == 'POST':
        duser = User.objects.get(username=doctorusername)
        doctor_profile = duser.doctor
        
        form = DoctorProfileUpdateForm(request.POST)
        if form.is_valid():
            try:
                # Parse dates
                dob_date = form.cleaned_data['dob']
                yor_date = form.cleaned_data['year_of_registration']
                
                # Update doctor profile
                doctor.objects.filter(pk=duser.doctor).update(
                    name=form.cleaned_data['name'],
                    dob=dob_date,
                    gender=form.cleaned_data['gender'],
                    address=form.cleaned_data['address'],
                    mobile_no=form.cleaned_data['mobile_no'],
                    registration_no=form.cleaned_data['registration_no'],
                    year_of_registration=yor_date,
                    qualification=form.cleaned_data['qualification'],
                    State_Medical_Council=form.cleaned_data['State_Medical_Council'],
                    specialization=form.cleaned_data['specialization']
                )
                
                messages.success(request, 'Profile updated successfully!')
                return redirect('dviewprofile', doctorusername)
                
            except Exception as e:
                messages.error(request, f'Error updating profile: {str(e)}. Please try again.')
                return redirect('dviewprofile', doctorusername)
        else:
            # Form has errors, display them
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.title()}: {error}')
            return redirect('dviewprofile', doctorusername)
    else:
        return redirect('dviewprofile', doctorusername)

