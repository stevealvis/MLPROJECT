from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator, MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import User
import re
from datetime import date

# Custom validators
def validate_username(value):
    """Validate username format"""
    if not re.match(r'^[a-zA-Z0-9_]+$', value):
        raise ValidationError('Username can only contain letters, numbers, and underscores.')
    if len(value) < 3:
        raise ValidationError('Username must be at least 3 characters long.')
    if len(value) > 30:
        raise ValidationError('Username cannot be more than 30 characters long.')

def validate_mobile_number(value):
    """Validate mobile number format"""
    # Remove all non-digits
    phone = re.sub(r'\D', '', value)
    if len(phone) != 10:
        raise ValidationError('Mobile number must be exactly 10 digits.')
    if not phone.startswith(('6', '7', '8', '9')):
        raise ValidationError('Mobile number must start with 6, 7, 8, or 9.')

def validate_registration_number(value):
    """Validate medical registration number format"""
    if len(value) < 6:
        raise ValidationError('Registration number must be at least 6 characters long.')
    if len(value) > 20:
        raise ValidationError('Registration number cannot be more than 20 characters long.')

def validate_password_strength(value):
    """Validate password strength"""
    if len(value) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    
    if not re.search(r'[A-Z]', value):
        raise ValidationError('Password must contain at least one uppercase letter.')
    
    if not re.search(r'[a-z]', value):
        raise ValidationError('Password must contain at least one lowercase letter.')
    
    if not re.search(r'\d', value):
        raise ValidationError('Password must contain at least one digit.')
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError('Password must contain at least one special character.')

def validate_dob(value):
    """Validate date of birth"""
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    
    if age < 13:
        raise ValidationError('You must be at least 13 years old to register.')
    if age > 120:
        raise ValidationError('Please enter a valid date of birth.')

class PatientSignupForm(forms.Form):
    """Professional patient signup form with comprehensive validation"""
    
    username = forms.CharField(
        max_length=30,
        validators=[validate_username],
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Username',
            'required': True,
            'autocomplete': 'username'
        })
    )
    
    email = forms.EmailField(
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={
            'class': 'input-field',
            'placeholder': 'Email Address',
            'required': True,
            'autocomplete': 'email'
        })
    )
    
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Full Name',
            'required': True
        })
    )
    
    dob = forms.DateField(
        validators=[validate_dob],
        widget=forms.DateInput(attrs={
            'class': 'input-field',
            'type': 'date',
            'required': True
        })
    )
    
    age = forms.IntegerField(
        min_value=13,
        max_value=120,
        widget=forms.NumberInput(attrs={
            'class': 'input-field',
            'placeholder': 'Age',
            'min': '13',
            'max': '120',
            'required': True
        })
    )
    
    gender = forms.ChoiceField(
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other')
        ],
        widget=forms.RadioSelect(attrs={
            'class': 'radio-btn',
            'required': True
        })
    )
    
    address = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Complete Address',
            'required': True
        })
    )
    
    mobile_no = forms.CharField(
        max_length=10,
        validators=[validate_mobile_number],
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Mobile Number',
            'required': True,
            'pattern': '[0-9]{10}',
            'title': 'Please enter 10 digit mobile number'
        })
    )
    
    password = forms.CharField(
        validators=[validate_password_strength],
        widget=forms.PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Password',
            'required': True,
            'title': 'Password must be at least 8 characters with uppercase, lowercase, number, and special character'
        })
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Confirm Password',
            'required': True
        })
    )
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email address is already registered.')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password1 = cleaned_data.get('password1')
        
        if password and password1 and password != password1:
            raise ValidationError('Passwords do not match.')
        
        return cleaned_data
    
    def clean_age(self):
        age = self.cleaned_data['age']
        dob = self.cleaned_data.get('dob')
        
        if dob:
            today = date.today()
            calculated_age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            
            if abs(age - calculated_age) > 1:  # Allow 1 year difference for approximation
                raise ValidationError('Age does not match the date of birth.')
        
        return age


class DoctorSignupForm(forms.Form):
    """Professional doctor signup form with comprehensive validation"""
    
    username = forms.CharField(
        max_length=30,
        validators=[validate_username],
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Username',
            'required': True,
            'autocomplete': 'username'
        })
    )
    
    email = forms.EmailField(
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={
            'class': 'input-field',
            'placeholder': 'Email Address',
            'required': True,
            'autocomplete': 'email'
        })
    )
    
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Full Name',
            'required': True
        })
    )
    
    dob = forms.DateField(
        validators=[validate_dob],
        widget=forms.DateInput(attrs={
            'class': 'input-field',
            'type': 'date',
            'required': True
        })
    )
    
    gender = forms.ChoiceField(
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other')
        ],
        widget=forms.RadioSelect(attrs={
            'class': 'radio-btn',
            'required': True
        })
    )
    
    address = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Complete Address',
            'required': True
        })
    )
    
    mobile_no = forms.CharField(
        max_length=10,
        validators=[validate_mobile_number],
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Mobile Number',
            'required': True,
            'pattern': '[0-9]{10}',
            'title': 'Please enter 10 digit mobile number'
        })
    )
    
    registration_no = forms.CharField(
        max_length=20,
        validators=[validate_registration_number],
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Medical Registration Number',
            'required': True,
            'title': 'Enter your medical registration number'
        })
    )
    
    year_of_registration = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'input-field',
            'type': 'date',
            'required': True
        })
    )
    
    qualification = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Qualification (e.g., MBBS, MD, etc.)',
            'required': True
        })
    )
    
    State_Medical_Council = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'State Medical Council',
            'required': True
        })
    )
    
    specialization = forms.ChoiceField(
        choices=[
            ('', 'Select Specialization'),
            ('Rheumatologist', 'Rheumatologist'),
            ('Cardiologist', 'Cardiologist'),
            ('ENT specialist', 'ENT Specialist'),
            ('Orthopedist', 'Orthopedist'),
            ('Neurologist', 'Neurologist'),
            ('Allergist/Immunologist', 'Allergist/Immunologist'),
            ('Urologist', 'Urologist'),
            ('Dermatologist', 'Dermatologist'),
            ('Gastroenterologist', 'Gastroenterologist'),
            ('General Physician', 'General Physician'),
            ('Pediatrician', 'Pediatrician'),
            ('Psychiatrist', 'Psychiatrist'),
            ('Oncologist', 'Oncologist'),
            ('Ophthalmologist', 'Ophthalmologist'),
            ('Other', 'Other'),
        ],
        widget=forms.Select(attrs={
            'class': 'select-field',
            'required': True
        })
    )
    
    password = forms.CharField(
        validators=[validate_password_strength],
        widget=forms.PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Password',
            'required': True,
            'title': 'Password must be at least 8 characters with uppercase, lowercase, number, and special character'
        })
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Confirm Password',
            'required': True
        })
    )
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email address is already registered.')
        return email
    
    def clean_year_of_registration(self):
        year_of_reg = self.cleaned_data['year_of_registration']
        dob = self.cleaned_data.get('dob')
        
        if year_of_reg and dob:
            # Doctor should be at least 24 years old when registering
            age_at_registration = year_of_reg.year - dob.year - ((year_of_reg.month, year_of_reg.day) < (dob.month, dob.day))
            if age_at_registration < 24:
                raise ValidationError('Invalid year of registration. You should be at least 24 years old when registering.')
            
            # Registration should not be in the future
            if year_of_reg > date.today():
                raise ValidationError('Registration year cannot be in the future.')
        
        return year_of_reg
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password1 = cleaned_data.get('password1')
        
        if password and password1 and password != password1:
            raise ValidationError('Passwords do not match.')
        
        return cleaned_data


class PatientProfileUpdateForm(forms.Form):
    """Form for updating patient profile"""
    
    name = forms.CharField(max_length=50, required=True)
    dob = forms.DateField(validators=[validate_dob], required=True)
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], required=True)
    address = forms.CharField(max_length=100, required=True)
    mobile_no = forms.CharField(max_length=10, validators=[validate_mobile_number], required=True)


class DoctorProfileUpdateForm(forms.Form):
    """Form for updating doctor profile"""
    
    name = forms.CharField(max_length=50, required=True)
    dob = forms.DateField(validators=[validate_dob], required=True)
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], required=True)
    address = forms.CharField(max_length=100, required=True)
    mobile_no = forms.CharField(max_length=10, validators=[validate_mobile_number], required=True)
    registration_no = forms.CharField(max_length=20, validators=[validate_registration_number], required=True)
    year_of_registration = forms.DateField(required=True)
    qualification = forms.CharField(max_length=20, required=True)
    State_Medical_Council = forms.CharField(max_length=30, required=True)
    specialization = forms.ChoiceField(choices=[
        ('', 'Select Specialization'),
        ('Rheumatologist', 'Rheumatologist'),
        ('Cardiologist', 'Cardiologist'),
        ('ENT specialist', 'ENT Specialist'),
        ('Orthopedist', 'Orthopedist'),
        ('Neurologist', 'Neurologist'),
        ('Allergist/Immunologist', 'Allergist/Immunologist'),
        ('Urologist', 'Urologist'),
        ('Dermatologist', 'Dermatologist'),
        ('Gastroenterologist', 'Gastroenterologist'),
        ('General Physician', 'General Physician'),
        ('Pediatrician', 'Pediatrician'),
        ('Psychiatrist', 'Psychiatrist'),
        ('Oncologist', 'Oncologist'),
        ('Ophthalmologist', 'Ophthalmologist'),
        ('Other', 'Other'),
    ], required=True)
