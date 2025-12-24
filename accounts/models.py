from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone

# Create your models here.

class Patient(models.Model):
    """Patient model corresponding to PatientSignupForm"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    
    # Personal Information
    name = models.CharField(max_length=50, help_text="Patient's full name")
    email = models.EmailField(help_text="Patient's email address")
    dob = models.DateField(help_text="Date of birth")
    age = models.PositiveIntegerField(help_text="Patient's age")
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, help_text="Patient's gender")
    
    # Contact Information
    address = models.TextField(help_text="Patient's complete residential address")
    mobile_no = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^[6789]\d{9}$', message="Enter a valid 10-digit mobile number starting with 6,7,8 or 9")],
        help_text="10-digit mobile number"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Patient: {self.name} ({self.user.username})"
    
    def get_age(self):
        """Calculate current age from DOB"""
        today = timezone.now().date()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
    
    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        ordering = ['-created_at']


class Doctor(models.Model):
    """Doctor model corresponding to DoctorSignupForm"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    
    # Personal Information
    name = models.CharField(max_length=50, help_text="Doctor's full name")
    email = models.EmailField(help_text="Doctor's email address")
    dob = models.DateField(help_text="Date of birth")
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, help_text="Doctor's gender")
    
    # Contact Information
    address = models.TextField(help_text="Doctor's complete residential address")
    mobile_no = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^[6789]\d{9}$', message="Enter a valid 10-digit mobile number starting with 6,7,8 or 9")],
        help_text="10-digit mobile number"
    )
    
    # Professional Information
    registration_no = models.CharField(
        max_length=20,
        help_text="Medical registration number",
        unique=True
    )
    year_of_registration = models.DateField(help_text="Year of medical registration")
    qualification = models.CharField(max_length=50, help_text="Medical qualification (e.g., MBBS, MD, MS)")
    State_Medical_Council = models.CharField(max_length=50, help_text="State Medical Council name")
    
    SPECIALIZATION_CHOICES = [
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
    ]
    specialization = models.CharField(max_length=30, choices=SPECIALIZATION_CHOICES, help_text="Medical specialization")
    
    # Professional Status
    is_verified = models.BooleanField(default=False, help_text="Whether doctor's credentials are verified")
    is_available = models.BooleanField(default=True, help_text="Whether doctor is currently available for appointments")
    years_of_experience = models.PositiveIntegerField(default=0, help_text="Years of medical experience")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Dr. {self.name} - {self.get_specialization_display()}"
    
    def get_age(self):
        """Calculate current age from DOB"""
        today = timezone.now().date()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
    
    def calculate_experience(self):
        """Calculate years of experience from registration date"""
        today = timezone.now().date()
        return today.year - self.year_of_registration.year
    
    def is_eligible_for_registration(self):
        """Check if doctor meets minimum age requirement for registration"""
        return self.get_age() >= 24
    
    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"
        ordering = ['-created_at']
        unique_together = ['registration_no']  # Ensure unique registration numbers


# Backward compatibility aliases for existing code
patient = Patient
doctor = Doctor

class UserProfile(models.Model):
    """Extended user profile for both patients and doctors"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Profile Information
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, help_text="User profile picture")
    bio = models.TextField(blank=True, help_text="User biography or description")
    
    # Preferences
    notification_preferences = models.JSONField(default=dict, blank=True, help_text="User notification preferences")
    privacy_settings = models.JSONField(default=dict, blank=True, help_text="User privacy settings")
    
    # Status
    is_profile_complete = models.BooleanField(default=False, help_text="Whether user has completed their profile")
    last_login_ip = models.GenericIPAddressField(blank=True, null=True, help_text="Last login IP address")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile: {self.user.username}"
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


class MedicalRecord(models.Model):
    """Medical records for patients (for future expansion)"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='medical_records')
    
    # Record Information
    record_type = models.CharField(max_length=50, help_text="Type of medical record")
    diagnosis = models.TextField(help_text="Medical diagnosis")
    treatment = models.TextField(help_text="Treatment provided")
    prescription = models.TextField(blank=True, help_text="Prescription details")
    notes = models.TextField(blank=True, help_text="Additional notes")
    
    # Dates
    record_date = models.DateTimeField(default=timezone.now, help_text="Date of medical record")
    follow_up_date = models.DateTimeField(blank=True, null=True, help_text="Follow-up appointment date")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_confidential = models.BooleanField(default=True, help_text="Whether record is confidential")
    
    def __str__(self):
        return f"Record: {self.patient.name} - {self.record_type} ({self.record_date.date()})"
    
    class Meta:
        verbose_name = "Medical Record"
        verbose_name_plural = "Medical Records"
        ordering = ['-record_date']


class Appointment(models.Model):
    """Appointment system for future expansion"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    
    # Appointment Details
    appointment_date = models.DateTimeField(help_text="Scheduled appointment date and time")
    duration_minutes = models.PositiveIntegerField(default=30, help_text="Appointment duration in minutes")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='scheduled')
    
    # Appointment Information
    reason = models.TextField(help_text="Reason for appointment")
    notes = models.TextField(blank=True, help_text="Additional appointment notes")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Appointment: {self.patient.name} with Dr. {self.doctor.name} on {self.appointment_date.date()}"
    
    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
        ordering = ['appointment_date']
        unique_together = ['doctor', 'appointment_date']  # Prevent double booking
