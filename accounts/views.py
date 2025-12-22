from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib import messages
from django.contrib.auth.models import User , auth
from .models import Patient, Doctor, UserProfile, MedicalRecord, Appointment
from datetime import datetime
from .forms import PatientSignupForm, DoctorSignupForm, PatientProfileUpdateForm, DoctorProfileUpdateForm

# Create your views here.


   
def logout(request):
    auth.logout(request)
    request.session.pop('patientid', None)
    request.session.pop('doctorid', None)
    request.session.pop('adminid', None)
    return render(request,'homepage/index.html')




def sign_in_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Validate input
        if not username or not password:
            messages.info(request, 'Please enter both username and password.')
            return redirect('sign_in_admin')

        # Authenticate user
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # Check if user is superuser (admin)
            if user.is_superuser and user.is_staff:
                auth.login(request, user)
                # Store admin info in session
                request.session['adminid'] = user.id
                request.session['admin_username'] = user.username
                
                messages.success(request, f'Welcome, {user.username}!')
                return redirect('admin_ui')
            else:
                messages.info(request, 'This account does not have admin privileges.')
                return redirect('sign_in_admin')
        else:
            messages.info(request, 'Invalid username or password. Please check your credentials.')
            return redirect('sign_in_admin')
    else:
        # Handle GET request - show login form
        return render(request, 'admin/signin/signin.html')



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
                
                # Create patient profile using new Django model
                patientnew = Patient(
                    user=user,
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    dob=dob_date,
                    age=form.cleaned_data['age'],
                    gender=form.cleaned_data['gender'],
                    address=form.cleaned_data['address'],
                    mobile_no=form.cleaned_data['mobile_no']
                )
                patientnew.save()
                
                # Create user profile
                UserProfile.objects.create(user=user)
                
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



def sign_in_patient(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            try:
                # Check if user has a patient profile
                patient_profile = user.patient_profile
                if patient_profile.is_active:
                    auth.login(request, user)
                    request.session['patientusername'] = user.username
                    return redirect('patient_ui')
                else:
                    messages.info(request, 'Your patient account is not active. Please contact support.')
                    return redirect('sign_in_patient')
            except Patient.DoesNotExist:
                messages.info(request, 'Invalid credentials or patient account does not exist.')
                return redirect('sign_in_patient')
        else:
            messages.info(request, 'Invalid credentials. Please check your username and password.')
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
                
                # Create doctor profile using new Django model
                doctornew = Doctor(
                    user=user,
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
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
                
                # Create user profile
                UserProfile.objects.create(user=user)
                
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








def sign_in_doctor(request):
    if request.method == 'GET':
        return render(request, 'doctor/signin_page/index.html')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            try:
                # Check if user has a doctor profile
                doctor_profile = user.doctor_profile
                if doctor_profile.is_active:
                    auth.login(request, user)
                    request.session['doctorusername'] = user.username
                    return redirect('doctor_ui')
                else:
                    messages.info(request, 'Your doctor account is not active. Please contact support.')
                    return redirect('sign_in_doctor')
            except Doctor.DoesNotExist:
                messages.info(request, 'Invalid credentials or doctor account does not exist.')
                return redirect('sign_in_doctor')
        else:
            messages.info(request, 'Invalid credentials. Please check your username and password.')
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

