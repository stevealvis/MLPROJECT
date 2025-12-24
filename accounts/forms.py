from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator, MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import User
import re
from datetime import date

# Indian States List
INDIAN_STATES = [
    ('', 'Select State'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
    ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
    ('Chandigarh', 'Chandigarh'),
    ('Dadra and Nagar Haveli and Daman and Diu', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('Delhi', 'Delhi'),
    ('Jammu and Kashmir', 'Jammu and Kashmir'),
    ('Ladakh', 'Ladakh'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Puducherry', 'Puducherry'),
]

# Major Indian Cities List
INDIAN_CITIES = [
    ('', 'Select City'),
    ('Mumbai', 'Mumbai'),
    ('Delhi', 'Delhi'),
    ('Bangalore', 'Bangalore'),
    ('Hyderabad', 'Hyderabad'),
    ('Chennai', 'Chennai'),
    ('Kolkata', 'Kolkata'),
    ('Pune', 'Pune'),
    ('Ahmedabad', 'Ahmedabad'),
    ('Jaipur', 'Jaipur'),
    ('Surat', 'Surat'),
    ('Lucknow', 'Lucknow'),
    ('Kanpur', 'Kanpur'),
    ('Nagpur', 'Nagpur'),
    ('Indore', 'Indore'),
    ('Thane', 'Thane'),
    ('Bhopal', 'Bhopal'),
    ('Visakhapatnam', 'Visakhapatnam'),
    ('Patna', 'Patna'),
    ('Vadodara', 'Vadodara'),
    ('Ghaziabad', 'Ghaziabad'),
    ('Ludhiana', 'Ludhiana'),
    ('Agra', 'Agra'),
    ('Nashik', 'Nashik'),
    ('Faridabad', 'Faridabad'),
    ('Meerut', 'Meerut'),
    ('Rajkot', 'Rajkot'),
    ('Varanasi', 'Varanasi'),
    ('Srinagar', 'Srinagar'),
    ('Amritsar', 'Amritsar'),
    ('Chandigarh', 'Chandigarh'),
    ('Jodhpur', 'Jodhpur'),
    ('Raipur', 'Raipur'),
    ('Kochi', 'Kochi'),
    ('Gwalior', 'Gwalior'),
    ('Vijayawada', 'Vijayawada'),
    ('Madurai', 'Madurai'),
    ('Guwahati', 'Guwahati'),
    ('Hubli', 'Hubli'),
    ('Mysore', 'Mysore'),
    ('Other', 'Other'),
]

# Custom validators
def validate_username(value):
    """Validate username format"""
    # Must start with a letter
    if not value or not value[0].isalpha():
        raise ValidationError('Username must start with a letter.')
    # Only letters, numbers, and underscores allowed (no spaces or other symbols)
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', value):
        raise ValidationError('Username can only contain letters, numbers, and underscores. No spaces or other symbols allowed.')
    # Length must be 5-20 characters
    if len(value) < 5:
        raise ValidationError('Username must be at least 5 characters long.')
    if len(value) > 20:
        raise ValidationError('Username cannot be more than 20 characters long.')

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
    """Validate password strength with enhanced security"""
    if len(value) < 6:
        raise ValidationError('Password must be at least 6 characters long.')
    
    if not re.search(r'[A-Z]', value):
        raise ValidationError('Password must contain at least one uppercase letter (A-Z).')
    
    if not re.search(r'[a-z]', value):
        raise ValidationError('Password must contain at least one lowercase letter (a-z).')
    
    if not re.search(r'\d', value):
        raise ValidationError('Password must contain at least one digit (0-9).')
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>_~`\-=+\[\]{};:|,./<>?]', value):
        raise ValidationError('Password must contain at least one special character.')
    
    # Check for common weak patterns (more specific to avoid false positives)
    common_weak_patterns = [
        '123456', 'password123', 'admin123', 'qwerty123', 'abc123456',
        'welcome123', 'test123', 'login123', '123456789', '1234567890',
        'password', 'admin', 'qwerty', 'abc123', '111111', '123123',
        '1234567890123456',  # Common long digit sequence
        'qwertyuiop',  # Keyboard sequences
        'asdfghjkl',   # Keyboard sequences
        'zxcvbnm'      # Keyboard sequences
    ]
    
    password_lower = value.lower()
    for pattern in common_weak_patterns:
        # More sophisticated pattern matching
        if pattern == 'password':
            # Only flag if it's exactly "password" (standalone)
            if password_lower == 'password':
                raise ValidationError('Password contains common weak patterns. Please choose a more secure password.')
        elif pattern in password_lower:
            # For other patterns, check if they appear at the beginning
            if password_lower.startswith(pattern):
                raise ValidationError('Password contains common weak patterns. Please choose a more secure password.')
    
    # Check for sequential characters (more lenient - only reject long sequences of 4+)
    if re.search(r'(0123|1234|2345|3456|4567|5678|6789|7890|abcd|bcde|cdef|defg|efgh|fghi)', value.lower()):
        raise ValidationError('Password cannot contain long sequential characters like 1234 or abcd.')
    
    # Check for repeated characters (more than 3 in a row)
    if re.search(r'(.)\1\1\1', value):
        raise ValidationError('Password cannot contain more than 3 repeated characters in a row.')
    
    # Ensure password is not too similar to username or email
    # This will be checked in the form's clean method where we have access to all fields

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
        max_length=20,
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
        required=False,  # Not required since it's auto-calculated
        widget=forms.NumberInput(attrs={
            'class': 'input-field',
            'placeholder': 'Age (auto-calculated)',
            'min': '13',
            'max': '120',
            'readonly': 'readonly',
            'style': 'background-color: #f8f9fa; cursor: not-allowed;'
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
    
    address_line = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Street Address, Building, Area',
            'required': True
        })
    )
    
    city = forms.ChoiceField(
        choices=INDIAN_CITIES,
        widget=forms.Select(attrs={
            'class': 'select-field',
            'required': True
        })
    )
    
    state = forms.ChoiceField(
        choices=INDIAN_STATES,
        widget=forms.Select(attrs={
            'class': 'select-field',
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
            'placeholder': 'Password (min 6 chars)',
            'required': True,
            'minlength': '6',
            'title': 'Password must be at least 6 characters and include uppercase, lowercase, number, and special character.'
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
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        address_line = cleaned_data.get('address_line')
        city = cleaned_data.get('city')
        state = cleaned_data.get('state')
        
        # Validate address components
        if not address_line:
            self.add_error('address_line', ValidationError('Please enter your street address.'))
        if not city or city == '':
            self.add_error('city', ValidationError('Please select a city.'))
        if not state or state == '':
            self.add_error('state', ValidationError('Please select a state.'))
        
        # Validate city-state relationship
        if city and state and city != '' and state != '':
            city_state_map = {
                'Mumbai': 'Maharashtra',
                'Pune': 'Maharashtra',
                'Nagpur': 'Maharashtra',
                'Nashik': 'Maharashtra',
                'Thane': 'Maharashtra',
                'Delhi': 'Delhi',
                'Bangalore': 'Karnataka',
                'Mysore': 'Karnataka',
                'Hubli': 'Karnataka',
                'Hyderabad': 'Telangana',
                'Chennai': 'Tamil Nadu',
                'Madurai': 'Tamil Nadu',
                'Kolkata': 'West Bengal',
                'Ahmedabad': 'Gujarat',
                'Surat': 'Gujarat',
                'Vadodara': 'Gujarat',
                'Rajkot': 'Gujarat',
                'Jaipur': 'Rajasthan',
                'Jodhpur': 'Rajasthan',
                'Lucknow': 'Uttar Pradesh',
                'Kanpur': 'Uttar Pradesh',
                'Agra': 'Uttar Pradesh',
                'Varanasi': 'Uttar Pradesh',
                'Ghaziabad': 'Uttar Pradesh',
                'Meerut': 'Uttar Pradesh',
                'Indore': 'Madhya Pradesh',
                'Bhopal': 'Madhya Pradesh',
                'Gwalior': 'Madhya Pradesh',
                'Visakhapatnam': 'Andhra Pradesh',
                'Vijayawada': 'Andhra Pradesh',
                'Patna': 'Bihar',
                'Ludhiana': 'Punjab',
                'Amritsar': 'Punjab',
                'Chandigarh': 'Chandigarh',
                'Srinagar': 'Jammu and Kashmir',
                'Raipur': 'Chhattisgarh',
                'Kochi': 'Kerala',
                'Guwahati': 'Assam',
                'Faridabad': 'Haryana',
            }
            
            # Allow "Other" city to be selected with any state
            if city != 'Other' and city in city_state_map:
                expected_state = city_state_map[city]
                if expected_state != state:
                    self.add_error('city', ValidationError(f'{city} is not in {state}. {city} is located in {expected_state}.'))
                    self.add_error('state', ValidationError(f'{city} is not in {state}. {city} is located in {expected_state}.'))
        
        # Combine address fields into single address string for database storage
        # Store in a non-field key to avoid Django rendering it as a form field
        if address_line and city and state:
            combined_address = f"{address_line}, {city}, {state}"
            # Store as '_address' to avoid Django treating it as a form field
            cleaned_data['_address'] = combined_address
            # Also store as 'address' for views compatibility
            cleaned_data['address'] = combined_address
        
        # Check password confirmation
        if password and password1 and password != password1:
            self.add_error('password1', ValidationError('Passwords do not match.'))
        
        # Check password similarity with username
        if password and username:
            password_lower = password.lower()
            username_lower = username.lower()
            
            # Check if password contains username (more than 3 characters)
            if len(username_lower) >= 3 and username_lower in password_lower:
                self.add_error('password', ValidationError('Password cannot contain your username.'))
            
            # Check similarity (80% or more similarity)
            if self.calculate_similarity(password_lower, username_lower) > 0.8:
                self.add_error('password', ValidationError('Password is too similar to your username.'))
        
        # Check password similarity with email
        if password and email:
            password_lower = password.lower()
            email_parts = email.lower().split('@')[0]  # Get part before @
            
            # Check if password contains email prefix
            if len(email_parts) >= 3 and email_parts in password_lower:
                self.add_error('password', ValidationError('Password cannot contain your email address.'))
            
            # Check similarity
            if self.calculate_similarity(password_lower, email_parts) > 0.8:
                self.add_error('password', ValidationError('Password is too similar to your email address.'))
        
        return cleaned_data
    
    def calculate_similarity(self, str1, str2):
        """Calculate similarity between two strings (0-1 scale)"""
        if not str1 or not str2:
            return 0
        
        # Simple character-based similarity
        common_chars = 0
        for char in set(str1):
            common_chars += min(str1.count(char), str2.count(char))
        
        total_chars = max(len(str1), len(str2))
        return common_chars / total_chars if total_chars > 0 else 0


class DoctorSignupForm(forms.Form):
    """Professional doctor signup form with comprehensive validation"""
    
    username = forms.CharField(
        max_length=20,
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
    
    address_line = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Street Address, Building, Area',
            'required': True
        })
    )
    
    city = forms.ChoiceField(
        choices=INDIAN_CITIES,
        widget=forms.Select(attrs={
            'class': 'select-field',
            'required': True
        })
    )
    
    state = forms.ChoiceField(
        choices=INDIAN_STATES,
        widget=forms.Select(attrs={
            'class': 'select-field',
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
    
    year_of_registration = forms.IntegerField(
        min_value=1950,
        max_value=None,  # Will be validated in clean method
        widget=forms.NumberInput(attrs={
            'class': 'input-field',
            'placeholder': 'Year of Registration (e.g., 2010)',
            'required': True,
            'min': '1950',
            'max': '9999'
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
    
    State_Medical_Council = forms.ChoiceField(
        choices=INDIAN_STATES,
        widget=forms.Select(attrs={
            'class': 'select-field',
            'required': True
        })
    )
    
    specialization = forms.ChoiceField(
        choices=[
            ('', 'Select Specialization'),
            ('Dermatologist', 'Dermatologist'),
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
            'placeholder': 'Password (min 6 chars)',
            'required': True,
            'minlength': '6',
            'title': 'Password must be at least 6 characters and include uppercase, lowercase, number, and special character.'
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
        year_value = self.cleaned_data['year_of_registration']
        dob = self.cleaned_data.get('dob')
        
        if year_value:
            # Convert year to date (January 1st of that year) for storage
            year_of_reg = date(year_value, 1, 1)
            
            # Registration should not be in the future
            if year_of_reg > date.today():
                raise ValidationError('Registration year cannot be in the future.')
            
            if dob:
                # Doctor should be at least 24 years old when registering
                age_at_registration = year_of_reg.year - dob.year - ((year_of_reg.month, year_of_reg.day) < (dob.month, dob.day))
                if age_at_registration < 24:
                    raise ValidationError('Invalid year of registration. You should be at least 24 years old when registering.')
            
            return year_of_reg
        
        return year_value
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password1 = cleaned_data.get('password1')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        address_line = cleaned_data.get('address_line')
        city = cleaned_data.get('city')
        state = cleaned_data.get('state')
        
        # Validate address components
        if not address_line:
            self.add_error('address_line', ValidationError('Please enter your street address.'))
        if not city or city == '':
            self.add_error('city', ValidationError('Please select a city.'))
        if not state or state == '':
            self.add_error('state', ValidationError('Please select a state.'))
        
        # Combine address fields into single address string for database storage
        # Store in a non-field key to avoid Django rendering it as a form field
        if address_line and city and state:
            combined_address = f"{address_line}, {city}, {state}"
            # Store as '_address' to avoid Django treating it as a form field
            cleaned_data['_address'] = combined_address
            # Also store as 'address' for views compatibility
            cleaned_data['address'] = combined_address
        
        # Check password confirmation
        if password and password1 and password != password1:
            self.add_error('password1', ValidationError('Passwords do not match.'))
        
        # Check password similarity with username
        if password and username:
            password_lower = password.lower()
            username_lower = username.lower()
            
            # Check if password contains username (more than 3 characters)
            if len(username_lower) >= 3 and username_lower in password_lower:
                self.add_error('password', ValidationError('Password cannot contain your username.'))
            
            # Check similarity (80% or more similarity)
            if self.calculate_similarity(password_lower, username_lower) > 0.8:
                self.add_error('password', ValidationError('Password is too similar to your username.'))
        
        # Check password similarity with email
        if password and email:
            password_lower = password.lower()
            email_parts = email.lower().split('@')[0]  # Get part before @
            
            # Check if password contains email prefix
            if len(email_parts) >= 3 and email_parts in password_lower:
                self.add_error('password', ValidationError('Password cannot contain your email address.'))
            
            # Check similarity
            if self.calculate_similarity(password_lower, email_parts) > 0.8:
                self.add_error('password', ValidationError('Password is too similar to your email address.'))
        
        return cleaned_data
    
    def calculate_similarity(self, str1, str2):
        """Calculate similarity between two strings (0-1 scale)"""
        if not str1 or not str2:
            return 0
        
        # Simple character-based similarity
        common_chars = 0
        for char in set(str1):
            common_chars += min(str1.count(char), str2.count(char))
        
        total_chars = max(len(str1), len(str2))
        return common_chars / total_chars if total_chars > 0 else 0


class PatientProfileUpdateForm(forms.Form):
    """Professional patient profile update form with comprehensive validation"""
    
    name = forms.CharField(
        max_length=50,
        required=True,
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
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Complete Address',
            'required': True
        })
    )
    
    mobile_no = forms.CharField(
        max_length=10,
        validators=[validate_mobile_number],
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Mobile Number',
            'required': True,
            'pattern': '[0-9]{10}',
            'title': 'Please enter 10 digit mobile number'
        })
    )
    
    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if len(name) < 2:
            raise ValidationError('Name must be at least 2 characters long.')
        if len(name) > 50:
            raise ValidationError('Name cannot be more than 50 characters long.')
        return name
    
    def clean_address(self):
        address = self.cleaned_data['address'].strip()
        if len(address) < 10:
            raise ValidationError('Address must be at least 10 characters long.')
        if len(address) > 100:
            raise ValidationError('Address cannot be more than 100 characters long.')
        return address


class DoctorProfileUpdateForm(forms.Form):
    """Professional doctor profile update form with comprehensive validation"""
    
    name = forms.CharField(
        max_length=50,
        required=True,
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
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Complete Address',
            'required': True
        })
    )
    
    mobile_no = forms.CharField(
        max_length=10,
        validators=[validate_mobile_number],
        required=True,
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
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Medical Registration Number',
            'required': True,
            'title': 'Enter your medical registration number'
        })
    )
    
    year_of_registration = forms.IntegerField(
        min_value=1950,
        max_value=None,  # Will be validated in clean method
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'input-field',
            'placeholder': 'Year of Registration (e.g., 2010)',
            'required': True,
            'min': '1950',
            'max': '9999'
        })
    )
    
    qualification = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Qualification (e.g., MBBS, MD, etc.)',
            'required': True
        })
    )
    
    State_Medical_Council = forms.ChoiceField(
        choices=INDIAN_STATES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'select-field',
            'required': True
        })
    )
    
    specialization = forms.ChoiceField(
        choices=[
            ('', 'Select Specialization'),
            ('Dermatologist', 'Dermatologist'),
        ],
        widget=forms.Select(attrs={
            'class': 'select-field',
            'required': True
        })
    )
    
    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if len(name) < 2:
            raise ValidationError('Name must be at least 2 characters long.')
        if len(name) > 50:
            raise ValidationError('Name cannot be more than 50 characters long.')
        return name
    
    def clean_address(self):
        address = self.cleaned_data['address'].strip()
        if len(address) < 10:
            raise ValidationError('Address must be at least 10 characters long.')
        if len(address) > 100:
            raise ValidationError('Address cannot be more than 100 characters long.')
        return address
    
    def clean_qualification(self):
        qualification = self.cleaned_data['qualification'].strip()
        if len(qualification) < 2:
            raise ValidationError('Qualification must be at least 2 characters long.')
        if len(qualification) > 20:
            raise ValidationError('Qualification cannot be more than 20 characters long.')
        return qualification
    
    def clean_State_Medical_Council(self):
        state = self.cleaned_data['State_Medical_Council']
        if not state or state == '':
            raise ValidationError('Please select a state.')
        return state
    
    def clean_year_of_registration(self):
        year_value = self.cleaned_data['year_of_registration']
        dob = self.cleaned_data.get('dob')
        
        if year_value:
            # Convert year to date (January 1st of that year) for storage
            year_of_reg = date(year_value, 1, 1)
            
            # Registration should not be in the future
            if year_of_reg > date.today():
                raise ValidationError('Registration year cannot be in the future.')
            
            if dob:
                # Doctor should be at least 24 years old when registering
                age_at_registration = year_of_reg.year - dob.year - ((year_of_reg.month, year_of_reg.day) < (dob.month, dob.day))
                if age_at_registration < 24:
                    raise ValidationError('Invalid year of registration. You should be at least 24 years old when registering.')
            
            return year_of_reg
        
        return year_value
