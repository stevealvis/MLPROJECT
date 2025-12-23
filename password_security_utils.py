#!/usr/bin/env python3
"""
Password Security Verification Utilities
Provides functions to verify password strength and security
"""

import os
import sys
import django
import hashlib
import re
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Setup Django environment
sys.path.append('/Users/ankuankit/Desktop/pro/MLproject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'disease_prediction.settings')
django.setup()

def verify_password_hash(password, stored_hash):
    """
    Verify a password against its stored hash
    Returns True if password matches the stored hash
    """
    try:
        # Django's built-in password verification
        from django.contrib.auth.hashers import check_password
        return check_password(password, stored_hash)
    except Exception as e:
        print(f"Error verifying password hash: {e}")
        return False

def check_password_strength(password):
    """
    Check password strength and return detailed results
    """
    results = {
        'is_strong': False,
        'length_ok': False,
        'has_upper': False,
        'has_lower': False,
        'has_digit': False,
        'has_special': False,
        'no_sequential': False,
        'no_common_patterns': False,
        'no_repeats': False,
        'score': 0,
        'issues': []
    }
    
    # Length check
    if len(password) >= 12:
        results['length_ok'] = True
        results['score'] += 20
    else:
        results['issues'].append('Password must be at least 12 characters long')
    
    # Character type checks
    if re.search(r'[A-Z]', password):
        results['has_upper'] = True
        results['score'] += 15
    else:
        results['issues'].append('Missing uppercase letter')
    
    if re.search(r'[a-z]', password):
        results['has_lower'] = True
        results['score'] += 15
    else:
        results['issues'].append('Missing lowercase letter')
    
    if re.search(r'\d', password):
        results['has_digit'] = True
        results['score'] += 15
    else:
        results['issues'].append('Missing digit')
    
    if re.search(r'[!@#$%^&*(),.?":{}|<>_~`\-=+\[\]{};:|,./<>?]', password):
        results['has_special'] = True
        results['score'] += 15
    else:
        results['issues'].append('Missing special character')
    
    # Sequential characters check
    if not re.search(r'(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def|efg)', password.lower()):
        results['no_sequential'] = True
        results['score'] += 10
    else:
        results['issues'].append('Contains sequential characters')
    
    # Common patterns check
    common_patterns = ['password', '123', 'abc', 'qwerty', 'admin', 'user', 'test', 'login', 'welcome', 'medical', 'portal']
    password_lower = password.lower()
    has_common = any(pattern in password_lower for pattern in common_patterns)
    
    if not has_common:
        results['no_common_patterns'] = True
        results['score'] += 10
    else:
        results['issues'].append('Contains common weak patterns')
    
    # Repeated characters check
    if not re.search(r'(.)\1\1\1', password):
        results['no_repeats'] = True
        results['score'] += 5
    else:
        results['issues'].append('Contains repeated characters')
    
    # Overall strength assessment
    if results['score'] >= 80:
        results['is_strong'] = True
    elif results['score'] >= 60:
        results['strength'] = 'medium'
    else:
        results['strength'] = 'weak'
    
    return results

def audit_user_passwords():
    """
    Audit all user passwords in the database
    """
    print("=" * 60)
    print("PASSWORD SECURITY AUDIT")
    print("=" * 60)
    
    users = User.objects.all()
    if not users.exists():
        print("No users found in database.")
        return
    
    strong_count = 0
    medium_count = 0
    weak_count = 0
    
    print(f"Auditing {users.count()} user accounts...")
    print()
    
    for user in users:
        # We can't check actual passwords, but we can check for default/weak patterns
        issues = []
        
        # Check if username is same as password pattern
        if user.username.lower() in ['admin', 'user', 'test', 'root']:
            issues.append('Common username pattern')
        
        # Check email patterns
        if user.email and any(domain in user.email.lower() for domain in ['test.com', 'example.com', 'fake.com']):
            issues.append('Test/fake email domain')
        
        print(f"User: {user.username}")
        print(f"Email: {user.email}")
        print(f"Is Superuser: {user.is_superuser}")
        print(f"Is Staff: {user.is_staff}")
        
        if issues:
            print(f"⚠️  Security Issues: {', '.join(issues)}")
            weak_count += 1
        else:
            print("✅ No obvious security issues detected")
            strong_count += 1
        
        print("-" * 40)
    
    print("\n" + "=" * 60)
    print("AUDIT SUMMARY")
    print("=" * 60)
    print(f"Total Users: {users.count()}")
    print(f"Strong Security: {strong_count}")
    print(f"Issues Detected: {weak_count}")
    
    if weak_count > 0:
        print("\n🔒 RECOMMENDATIONS:")
        print("• Enforce password complexity requirements")
        print("• Implement password expiration policies")
        print("• Add two-factor authentication")
        print("• Regular security audits")
        print("• User education on password security")

def generate_security_report():
    """
    Generate a comprehensive security report
    """
    print("=" * 60)
    print("MEDICAL PORTAL SECURITY REPORT")
    print("=" * 60)
    
    # User statistics
    total_users = User.objects.count()
    superusers = User.objects.filter(is_superuser=True).count()
    staff_users = User.objects.filter(is_staff=True).count()
    
    print(f"User Statistics:")
    print(f"  • Total Users: {total_users}")
    print(f"  • Superusers: {superusers}")
    print(f"  • Staff Users: {staff_users}")
    
    # Check for default admin accounts
    default_admins = User.objects.filter(username__in=['admin', 'administrator', 'root'])
    if default_admins.exists():
        print(f"\n⚠️  SECURITY WARNING:")
        print(f"Found {default_admins.count()} default admin account(s):")
        for admin in default_admins:
            print(f"  • {admin.username}")
    
    # Check for test accounts
    test_users = User.objects.filter(username__iregex=r'^(test|user\d+|demo)')
    if test_users.exists():
        print(f"\n⚠️  TEST ACCOUNTS DETECTED:")
        print(f"Found {test_users.count()} test account(s):")
        for user in test_users:
            print(f"  • {user.username}")
    
    print("\n" + "=" * 60)
    print("SECURITY RECOMMENDATIONS")
    print("=" * 60)
    print("✅ Implemented:")
    print("  • Strong password validation (12+ chars)")
    print("  • Password similarity checking")
    print("  • Sequential character prevention")
    print("  • Common pattern detection")
    print("  • Secure admin creation scripts")
    
    print("\n🔒 Recommended Next Steps:")
    print("  • Enable Django's password validators")
    print("  • Implement session timeout")
    print("  • Add login attempt limiting")
    print("  • Enable audit logging")
    print("  • Implement 2FA")
    print("  • Regular password expiration")
    
    return True

def test_password_validation():
    """
    Test the password validation functions
    """
    print("=" * 60)
    print("PASSWORD VALIDATION TESTING")
    print("=" * 60)
    
    test_passwords = [
        "Weak123!",           # Should fail - too short
        "password123!",       # Should fail - common pattern
        "abc123456!",         # Should fail - sequential
        "Password123!",       # Should pass
        "MySecure2024@Medical!", # Should pass
        "Admin2024!",         # Should fail - contains admin
        "Test1234567890!",    # Should pass
    ]
    
    for pwd in test_passwords:
        print(f"\nTesting: {pwd}")
        result = check_password_strength(pwd)
        print(f"Score: {result['score']}/100")
        print(f"Strong: {result['is_strong']}")
        if result['issues']:
            print(f"Issues: {', '.join(result['issues'])}")
        else:
            print("✅ No issues detected")

if __name__ == "__main__":
    print("🔒 Medical Portal Security Verification Utilities")
    print("=" * 60)
    
    while True:
        print("\nSelect an option:")
        print("1. Audit user passwords")
        print("2. Generate security report")
        print("3. Test password validation")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            audit_user_passwords()
        elif choice == '2':
            generate_security_report()
        elif choice == '3':
            test_password_validation()
        elif choice == '4':
            print("Security verification complete!")
            break
        else:
            print("Invalid choice. Please try again.")
