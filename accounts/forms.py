from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator, MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import User
from django.utils.html import escape
from .models import Patient, Doctor, UserProfile
import re
import html
from datetime import date

# Security-focused custom validators
def sanitize_input(value):
    """OWASP A03: Injection Prevention - Input Sanitization"""
    if value is None:
        return value
    # Remove null bytes and control characters
    sanitized = ''.join(char for char in str(value) if ord(char) >= 32 or char in ['\n', '\r', '\t'])
    # HTML escape to prevent XSS
    return html.escape(sanitized.strip())

def validate_username(value):
    """OWASP A03: Injection & A07: Authentication - Enhanced username validation"""
    # Input sanitization first
    sanitized_value = sanitize_input(value)
    
    if len(sanitized_value) < 3:
        raise ValidationError('Username must be at least 3 characters long.')
    if len(sanitized_value) > 30:
        raise ValidationError('Username cannot be more than 30 characters long.')
    
    # Strict character whitelist (OWASP A03: Injection prevention)
    if not re.match(r'^[a-z0-9_.]+$', sanitized_value):
        raise ValidationError('Username can only contain lowercase letters, numbers, underscores, and dots.')
    
    # Username cannot start or end with underscore or dot
    if sanitized_value.startswith(('_', '.')) or sanitized_value.endswith(('_', '.')):
        raise ValidationError('Username cannot start or end with underscore or dot.')
    
    # Cannot have consecutive underscores or dots
    if '__' in sanitized_value or '..' in sanitized_value:
        raise ValidationError('Username cannot contain consecutive underscores or dots.')
    
    # Reserved usernames (OWASP A07: Authentication Failures prevention)
    reserved_usernames = ['admin', 'administrator', 'root', 'system', 'support', 'help', 'info', 'contact', 'test', 'demo']
    if sanitized_value in reserved_usernames:
        raise ValidationError('This username is reserved and cannot be used.')
    
    # Check for SQL injection patterns (OWASP A03: Injection prevention)
    sql_patterns = ['union', 'select', 'insert', 'delete', 'update', 'drop', 'alter', 'create', 'exec', 'execute', '--', ';', '/*', '*/']
    for pattern in sql_patterns:
        if pattern in sanitized_value.lower():
            raise ValidationError('Username contains prohibited patterns.')
    
    # Check for XSS patterns (OWASP A03: Injection prevention)
    xss_patterns = ['<script', 'javascript:', 'vbscript:', 'onload', 'onerror', 'onclick', '<iframe', '<object', '<embed']
    for pattern in xss_patterns:
        if pattern.lower() in sanitized_value.lower():
            raise ValidationError('Username contains prohibited characters.')
    
    return sanitized_value

def validate_mobile_number(value):
    """Validate mobile number format"""
    # Remove all non-digits
    phone = re.sub(r'\D', '', value)
    if len(phone) != 10:
        raise ValidationError('Mobile number must be exactly 10 digits.')
    if not phone.startswith(('6', '7', '8', '9')):
        raise ValidationError('Mobile number must start with 6, 7, 8, or 9.')

def validate_registration_number(value):
    """OWASP A03: Injection - Medical registration number validation with security checks"""
    # Input sanitization
    sanitized_value = sanitize_input(value)
    # Convert to uppercase for consistency
    sanitized_value = sanitized_value.upper()
    
    if len(sanitized_value) < 6:
        raise ValidationError('Registration number must be at least 6 characters long.')
    if len(sanitized_value) > 20:
        raise ValidationError('Registration number cannot be more than 20 characters long.')
    
    # Must contain both letters and numbers
    if not re.search(r'[A-Z]', sanitized_value) or not re.search(r'[0-9]', sanitized_value):
        raise ValidationError('Registration number must contain both letters and numbers.')
    
    # OWASP A03: Strict character whitelist
    if not re.match(r'^[A-Z0-9\-]+$', sanitized_value):
        raise ValidationError('Registration number can only contain letters, numbers, and hyphens.')
    
    # Check for excessive repeated characters
    if re.search(r'(.)\1{3,}', sanitized_value):
        raise ValidationError('Registration number cannot contain excessive repeated characters.')
    
    # OWASP A03: Check for SQL injection patterns
    sql_patterns = ['union', 'select', 'insert', 'delete', 'update', 'drop', 'alter', 'create', 'exec', 'execute']
    for pattern in sql_patterns:
        if pattern in sanitized_value.lower():
            raise ValidationError('Registration number contains prohibited patterns.')
    
    return sanitized_value

def validate_medical_council(value):
    """OWASP A03: Injection - State Medical Council validation with security checks"""
    # Input sanitization
    sanitized_value = sanitize_input(value)
    
    if len(sanitized_value) < 3:
        raise ValidationError('State Medical Council name must be at least 3 characters long.')
    if len(sanitized_value) > 50:
        raise ValidationError('State Medical Council name cannot be more than 50 characters long.')
    
    # OWASP A03: Check for valid characters (letters, spaces, hyphens)
    if not re.match(r'^[a-zA-Z\s\-]+$', sanitized_value):
        raise ValidationError('State Medical Council name can only contain letters, spaces, and hyphens.')
    
    # Validate against known Indian Medical Councils
    known_councils = [
        'andhra medical council', 'arunachal pradesh medical council', 'assam medical council',
        'bihar medical council', 'chhattisgarh medical council', 'goa medical council',
        'gujarat medical council', 'haryana medical council', 'himachal pradesh medical council',
        'jharkhand medical council', 'karnataka medical council', 'kerala medical council',
        'madhya pradesh medical council', 'maharashtra medical council', 'manipur medical council',
        'meghalaya medical council', 'mizoram medical council', 'nagaland medical council',
        'odisha medical council', 'punjab medical council', 'rajasthan medical council',
        'sikkim medical council', 'tamil nadu medical council', 'telangana medical council',
        'tripura medical council', 'uttar pradesh medical council', 'uttarakhand medical council',
        'west bengal medical council', 'delhi medical council', 'puducherry medical council'
    ]
    
    council_lower = sanitized_value.lower()
    is_valid_council = False
    for council in known_councils:
        if council in council_lower or council_lower in council:
            is_valid_council = True
            break
    
    # Allow custom councils but with validation
    if not is_valid_council and len(council_lower.split()) < 2:
        raise ValidationError('Please provide a valid State Medical Council name.')
    
    return sanitized_value

def validate_qualification(value):
    """OWASP A03: Injection - Medical qualification validation with security checks"""
    # Input sanitization
    sanitized_value = sanitize_input(value)
    
    if len(sanitized_value) < 2:
        raise ValidationError('Qualification must be at least 2 characters long.')
    if len(sanitized_value) > 50:
        raise ValidationError('Qualification cannot be more than 50 characters long.')
    
    # OWASP A03: Check for valid characters
    if not re.match(r'^[a-zA-Z\s\.\,\(\)]+$', sanitized_value):
        raise ValidationError('Qualification can only contain letters, spaces, dots, commas, and parentheses.')
    
    # Validate against known medical qualifications
    known_qualifications = [
        'mbbs', 'bds', 'bams', 'bhms', 'bums', 'md', 'ms', 'dm', 'mch', 'dnb', 'dgo', 'dch', 'dortho',
        'dcard', 'dneurology', 'dsurgery', 'danaesthesia', 'dophthalmology', 'dpsychiatry',
        'ddermatology', 'dgastroenterology', 'dnephrology', 'dendocrinology', 'drheumatology',
        'doncology', 'dcardiology', 'dneurology', 'dpediatrics', 'dgynaecology', 'dorthopaedics',
        'dent', 'dophthalmology', 'dpsychiatry', 'danaesthesia', 'dradiology', 'dpathology',
        'dmicrobiology', 'dbiochemistry', 'dpharmacology', 'dphysiology', 'danatomy', 'dforensic'
    ]
    
    qual_lower = sanitized_value.lower()
    is_valid_qual = False
    for qual in known_qualifications:
        if qual in qual_lower:
            is_valid_qual = True
            break
    
    # Allow other medical qualifications but validate format
    if not is_valid_qual:
        # OWASP A03: Check for common medical degree patterns
        if not re.search(r'\b(mbbs|bds|m\.d|m\.s|d\.m|m\.ch|d\.n\.b|b\.a\.m\.s|b\.h\.m\.s)\b', qual_lower):
            raise ValidationError('Please provide a valid medical qualification.')
    
    return sanitized_value

def validate_password_strength(value):
    """OWASP A07: Authentication Failures - Enhanced password validation"""
    errors = []
    
    # OWASP A07: Strong password requirements
    if len(value) < 12:
        errors.append('Password must be at least 12 characters long.')
    elif len(value) > 128:
        errors.append('Password cannot be more than 128 characters long.')
    
    if not re.search(r'[a-z]', value):
        errors.append('Password must contain at least one lowercase letter.')
    
    if not re.search(r'[A-Z]', value):
        errors.append('Password must contain at least one uppercase letter.')
    
    if not re.search(r'\d', value):
        errors.append('Password must contain at least one number.')
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'"\\|,.<>\/?]', value):
        errors.append('Password must contain at least one special character.')
    
    # OWASP A07: Pattern detection for common attack vectors
    if re.search(r'(.)\1{2,}', value):  # Three or more repeated characters
        errors.append('Password cannot contain three or more consecutive identical characters.')
    
    # OWASP A07: Sequential pattern detection
    sequential_patterns = [
        '0123', '1234', '2345', '3456', '4567', '5678', '6789', '7890',
        'abcd', 'bcde', 'cdef', 'defg', 'efgh', 'fghi', 'ghij', 'hijk', 
        'ijkl', 'jklm', 'klmn', 'lmno', 'mnop', 'nopq', 'opqr', 'pqrs', 
        'qrst', 'rstu', 'stuv', 'tuvw', 'uvwx', 'vwxy', 'wxyz'
    ]
    for pattern in sequential_patterns:
        if pattern in value.lower():
            errors.append(f'Password cannot contain sequential patterns like {pattern}.')
            break
    
    # OWASP A07: Common password list check (simplified version)
    # In production, use a comprehensive password dictionary
    common_passwords = [
        'password', 'password1', 'password123', '123456', '12345678', '123456789',
        'qwerty', 'qwerty123', 'asdf', 'asdf123', 'zxcv', 'zxcv123',
        'admin', 'admin123', 'user', 'user123', 'login', 'login123',
        'welcome', 'welcome123', 'monkey', 'dragon', 'letmein',
        'abc123', '111111', '123123', 'iloveyou', 'football', 'baseball',
        'shadow', 'master', 'superman', 'hello', 'freedom'
    ]
    for common_pass in common_passwords:
        if common_pass in value.lower():
            errors.append(f'Password cannot be a common password like "{common_pass}".')
            break
    
    # OWASP A07: Check for date patterns (birth years, etc.)
    current_year = date.today().year
    for year in range(current_year - 100, current_year + 1):
        if str(year) in value:
            errors.append('Password cannot contain years or dates.')
            break
    
    # OWASP A07: Check for keyboard patterns
    keyboard_patterns = ['qwerty', 'asdf', 'zxcv', '1234', '9876', '!@#$']
    for pattern in keyboard_patterns:
        if pattern in value.lower():
            errors.append(f'Password cannot contain keyboard patterns like "{pattern}".')
            break
    
    if errors:
        raise ValidationError(errors)

def validate_dob(value):
    """Enhanced DOB validation like real medical portals"""
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    
    # Check if date is in the future
    if value > today:
        raise ValidationError('Date of birth cannot be in the future.')
    
    # Check if date is too old (unrealistic)
    if age > 100:
        raise ValidationError('Please enter a valid date of birth. You appear to be over 100 years old.')
    
    # Check minimum age based on user type (this will be handled in form validation)
    if age < 18:
        raise ValidationError('You must be at least 18 years old to register.')
    
    # Additional checks for reasonable dates
    if value.year < 1924:  # No one should be over 100
        raise ValidationError('Please enter a valid date of birth.')
    
    if value.year > today.year - 18:  # Must be at least 18
        raise ValidationError('You must be at least 18 years old to register.')
    
    return value

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
            'placeholder': 'Medical Registration Number (e.g., ABC123456)',
            'required': True,
            'title': 'Enter your medical registration number with letters and numbers'
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
        max_length=50,
        validators=[validate_qualification],
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Qualification (e.g., MBBS, MD Medicine, MS Orthopedics)',
            'required': True,
            'title': 'Enter your complete medical qualification'
        })
    )
    
    State_Medical_Council = forms.CharField(
        max_length=50,
        validators=[validate_medical_council],
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'State Medical Council (e.g., Maharashtra Medical Council)',
            'required': True,
            'title': 'Enter your state medical council name'
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
