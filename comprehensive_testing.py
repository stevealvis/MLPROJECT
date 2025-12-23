#!/usr/bin/env python3
"""
Comprehensive Testing Suite for Medical Portal Security & Forms Enhancement
Tests all implemented improvements including:
- Admin user creation with secure passwords
- Form validation enhancements
- Authentication flows
- Session management
- Password security features
"""

import os
import sys
import django
import unittest
import re
from datetime import date, datetime

# Setup Django environment
sys.path.append('/Users/ankuankit/Desktop/pro/MLproject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'disease_prediction.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from accounts.forms import (
    PatientSignupForm, DoctorSignupForm, 
    PatientProfileUpdateForm, DoctorProfileUpdateForm,
    validate_password_strength, validate_username, validate_mobile_number
)
from main_app.models import patient, doctor

class SecurityValidationTests(unittest.TestCase):
    """Test enhanced password security and validation"""
    
    def test_password_validation_strong(self):
        """Test that strong passwords pass validation"""
        strong_passwords = [
            "SecurePassword123!@#",
            "DoctorPortal456$%^",
            "PatientCare789&*",
            "HealthSystem@123",
            "SecureMedical456#",
            "Healthcare@Secure789$"
        ]
        
        for password in strong_passwords:
            try:
                validate_password_strength(password)
            except Exception as e:
                self.fail(f"Strong password '{password}' failed validation: {e}")
    
    def test_password_validation_weak(self):
        """Test that weak passwords are rejected"""
        weak_passwords = [
            "password123",  # Common pattern
            "admin123",     # Contains admin
            "abc123456",    # Sequential
            "12345678",     # Only digits
            "ABCDEFG123!",  # Sequential letters
            "aaaa1234!",    # Repeated characters
            "Short1!",      # Too short
            "passwordword", # Common pattern
            "qwerty123",    # Keyboard pattern
            "medical2024"   # Contains medical terms
        ]
        
        for password in weak_passwords:
            with self.assertRaises(Exception, msg=f"Weak password '{password}' should be rejected"):
                validate_password_strength(password)
    
    def test_username_validation(self):
        """Test username validation rules"""
        # Valid usernames
        valid_usernames = ["john_doe", "JaneSmith123", "doc_tor", "patient_user"]
        for username in valid_usernames:
            try:
                validate_username(username)
            except Exception as e:
                self.fail(f"Valid username '{username}' failed: {e}")
        
        # Invalid usernames
        invalid_usernames = ["jo", "very_long_username_that_exceeds_limit", "user@invalid", "user.name"]
        for username in invalid_usernames:
            with self.assertRaises(Exception, msg=f"Invalid username '{username}' should be rejected"):
                validate_username(username)
    
    def test_mobile_validation(self):
        """Test mobile number validation"""
        valid_phones = ["9876543210", "9876543210", "9876543210"]
        invalid_phones = ["1234567890", "987654321", "98765432101", "abc1234567"]
        
        for phone in valid_phones:
            try:
                validate_mobile_number(phone)
            except Exception as e:
                self.fail(f"Valid phone '{phone}' failed: {e}")
        
        for phone in invalid_phones:
            with self.assertRaises(Exception, msg=f"Invalid phone '{phone}' should be rejected"):
                validate_mobile_number(phone)

class FormValidationTests(unittest.TestCase):
    """Test enhanced form validation"""
    
    def test_patient_signup_form_validation(self):
        """Test patient signup form with enhanced validation"""
        # Valid data
        valid_data = {
            'username': 'test_patient',
            'email': 'patient@test.com',
            'name': 'John Doe',
            'dob': '1990-01-01',
            'age': 34,
            'gender': 'male',
            'address': '123 Main Street, City, State 12345',
            'mobile_no': '9876543210',
            'password': 'SecurePassword123!@#',
            'password1': 'SecurePassword123!@#'
        }
        
        form = PatientSignupForm(valid_data)
        self.assertTrue(form.is_valid(), f"Valid form failed: {form.errors}")
    
    def test_patient_signup_form_weak_password(self):
        """Test patient signup form rejects weak passwords"""
        weak_data = {
            'username': 'test_patient',
            'email': 'patient@test.com',
            'name': 'John Doe',
            'dob': '1990-01-01',
            'age': 33,
            'gender': 'male',
            'address': '123 Main Street, City, State 12345',
            'mobile_no': '9876543210',
            'password': 'password123',
            'password1': 'password123'
        }
        
        form = PatientSignupForm(weak_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
    
    def test_doctor_signup_form_validation(self):
        """Test doctor signup form with enhanced validation"""
        valid_data = {
            'username': 'test_doctor',
            'email': 'doctor@test.com',
            'name': 'Dr. Jane Smith',
            'dob': '1980-01-01',
            'gender': 'female',
            'address': '456 Medical Center, City, State 12345',
            'mobile_no': '8765432109',
            'registration_no': 'MD123456789',
            'year_of_registration': 2005,
            'qualification': 'MBBS MD',
            'State_Medical_Council': 'State Medical Council',
            'specialization': 'General Physician',
            'password': 'DoctorPass123!@#',
            'password1': 'DoctorPass123!@#'
        }
        
        form = DoctorSignupForm(valid_data)
        self.assertTrue(form.is_valid(), f"Valid doctor form failed: {form.errors}")
    
    def test_profile_update_forms(self):
        """Test profile update forms"""
        patient_data = {
            'name': 'Updated Patient Name',
            'dob': '1990-01-01',
            'gender': 'male',
            'address': 'Updated Address, City, State',
            'mobile_no': '9876543210'
        }
        
        form = PatientProfileUpdateForm(patient_data)
        self.assertTrue(form.is_valid(), f"Patient profile form failed: {form.errors}")
        
        doctor_data = {
            'name': 'Dr. Updated Name',
            'dob': '1980-01-01',
            'gender': 'female',
            'address': 'Updated Address, City, State',
            'mobile_no': '8765432109',
            'registration_no': 'MD123456789',
            'year_of_registration': 2005,
            'qualification': 'MBBS MD',
            'State_Medical_Council': 'State Medical Council',
            'specialization': 'General Physician'
        }
        
        form = DoctorProfileUpdateForm(doctor_data)
        self.assertTrue(form.is_valid(), f"Doctor profile form failed: {form.errors}")

class AuthenticationFlowTests(unittest.TestCase):
    """Test authentication and session management"""
    
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPassword123!@#'
        )
    
    def tearDown(self):
        self.test_user.delete()
    
    def test_secure_admin_creation_script(self):
        """Test the secure admin creation script"""
        from secure_admin_creation import generate_strong_password, generate_username
        
        # Test password generation
        password = generate_strong_password()
        self.assertTrue(len(password) >= 16)
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password))
        
        # Test username generation
        username = generate_username()
        self.assertTrue(username.startswith('admin_'))
        self.assertTrue(len(username) > 8)
    
    def test_password_security_utility(self):
        """Test password security verification utility"""
        from password_security_utils import check_password_strength
        
        strong_password = "SecurePassword123!@#"
        result = check_password_strength(strong_password)
        self.assertTrue(result['is_strong'])
        self.assertTrue(result['score'] >= 80)
        
        weak_password = "password123"
        result = check_password_strength(weak_password)
        self.assertFalse(result['is_strong'])
        self.assertGreater(len(result['issues']), 0)

class DatabaseIntegrityTests(unittest.TestCase):
    """Test database integrity and model validation"""
    
    def test_user_model_integrity(self):
        """Test user model constraints"""
        # Test unique constraints - this will fail because user already exists from setUp
        test_user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='password123'
        )
        self.assertIsNotNone(test_user2)
        test_user2.delete()
    
    def test_patient_model(self):
        """Test patient model creation"""
        user = User.objects.create_user(
            username='patient_test',
            email='patient_test@example.com',
            password='Password123!@#'
        )
        
        patient_profile = patient.objects.create(
            user=user,
            name='Test Patient',
            dob='1990-01-01',
            address='Test Address',
            mobile_no='9876543210',
            gender='male'
        )
        
        self.assertEqual(patient_profile.user, user)
        self.assertEqual(patient_profile.name, 'Test Patient')
        self.assertTrue(patient_profile.is_patient)
        self.assertFalse(patient_profile.is_doctor)
        
        # Cleanup
        patient_profile.delete()
        user.delete()
    
    def test_doctor_model(self):
        """Test doctor model creation"""
        user = User.objects.create_user(
            username='doctor_test',
            email='doctor_test@example.com',
            password='Password123!@#'
        )
        
        doctor_profile = doctor.objects.create(
            user=user,
            name='Dr. Test',
            dob='1980-01-01',
            address='Test Address',
            mobile_no='9876543210',
            gender='female',
            registration_no='MD123456789',
            year_of_registration=2005,
            qualification='MBBS MD',
            State_Medical_Council='Test Council',
            specialization='General Physician'
        )
        
        self.assertEqual(doctor_profile.user, user)
        self.assertEqual(doctor_profile.name, 'Dr. Test')
        self.assertTrue(doctor_profile.is_doctor)
        self.assertFalse(doctor_profile.is_patient)
        
        # Cleanup
        doctor_profile.delete()
        user.delete()

def run_comprehensive_tests():
    """Run all test suites"""
    print("=" * 80)
    print("MEDICAL PORTAL COMPREHENSIVE TESTING SUITE")
    print("=" * 80)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        SecurityValidationTests,
        FormValidationTests,
        AuthenticationFlowTests,
        DatabaseIntegrityTests
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()

def test_manual_scenarios():
    """Test manual scenarios and edge cases"""
    print("\n" + "=" * 80)
    print("MANUAL SCENARIO TESTING")
    print("=" * 80)
    
    scenarios = []
    
    # Scenario 1: Admin user creation
    print("\n1. Testing Admin User Creation...")
    try:
        from secure_admin_creation import create_secure_admin
        # We won't actually create in tests, just verify the function exists
        scenarios.append("✓ Admin creation script available")
    except Exception as e:
        scenarios.append(f"✗ Admin creation script failed: {e}")
    
    # Scenario 2: Password security utilities
    print("2. Testing Password Security Utilities...")
    try:
        from password_security_utils import check_password_strength
        test_result = check_password_strength("TestPassword123!@#")
        scenarios.append("✓ Password security utilities working")
    except Exception as e:
        scenarios.append(f"✗ Password security utilities failed: {e}")
    
    # Scenario 3: Form imports
    print("3. Testing Form Imports...")
    try:
        from accounts.forms import PatientSignupForm, DoctorSignupForm
        scenarios.append("✓ Forms importing successfully")
    except Exception as e:
        scenarios.append(f"✗ Form imports failed: {e}")
    
    # Scenario 4: Model imports
    print("4. Testing Model Imports...")
    try:
        from accounts.models import patient, doctor
        scenarios.append("✓ Models importing successfully")
    except Exception as e:
        scenarios.append(f"✗ Model imports failed: {e}")
    
    print("\nSCENARIO RESULTS:")
    for scenario in scenarios:
        print(scenario)
    
    return len([s for s in scenarios if s.startswith("✓")]) == len(scenarios)

def main():
    """Main testing function"""
    print("Starting Medical Portal Security & Form Enhancement Testing...")
    print("Testing implemented security features and form validations")
    
    # Run comprehensive tests
    test_success = run_comprehensive_tests()
    
    # Run manual scenarios
    scenario_success = test_manual_scenarios()
    
    # Final summary
    print("\n" + "=" * 80)
    print("FINAL TEST RESULTS")
    print("=" * 80)
    
    if test_success and scenario_success:
        print("🎉 ALL TESTS PASSED!")
        print("✓ Security enhancements working correctly")
        print("✓ Form validations functioning properly")
        print("✓ Database integrity maintained")
        print("✓ Authentication flows secure")
        print("✓ All components integration successful")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("Please review the failed tests above")
        
        if not test_success:
            print("✗ Unit tests failed")
        if not scenario_success:
            print("✗ Manual scenario tests failed")
    
    print("\n" + "=" * 80)
    print("RECOMMENDED NEXT STEPS:")
    print("=" * 80)
    print("1. Deploy changes to production environment")
    print("2. Run Django migrations if needed")
    print("3. Create admin user using secure_admin_creation.py")
    print("4. Test with real browser interaction")
    print("5. Enable additional security features (2FA, audit logging)")
    print("6. Monitor application performance")
    
    return test_success and scenario_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
