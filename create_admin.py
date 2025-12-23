#!/usr/bin/env python
"""
⚠️ DEPRECATED SCRIPT - INSECURE PASSWORD
This script creates admin users with weak, hardcoded passwords.
Use secure_admin_creation.py instead for production use.
"""
import os
import django
import secrets
import string

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'disease_prediction.settings')
django.setup()

from django.contrib.auth.models import User

def generate_secure_password():
    """Generate a secure random password"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(secrets.choice(chars) for _ in range(16))

def create_admin_with_secure_password():
    """Create admin user with secure password"""
    if not User.objects.filter(username='admin').exists():
        # Generate secure password
        secure_password = generate_secure_password()
        
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@secure-portal.com',
            password=secure_password
        )
        
        print("⚠️  INSECURE SCRIPT USED - GENERATED SECURE PASSWORD")
        print("=" * 50)
        print("Admin user created successfully!")
        print(f"Username: admin")
        print(f"Generated Password: {secure_password}")
        print("=" * 50)
        print("🔒 SECURITY RECOMMENDATIONS:")
        print("• Save this password securely")
        print("• Change password after first login")
        print("• Consider using secure_admin_creation.py instead")
        print("• Enable 2FA for additional security")
        print("=" * 50)
        
        # Save to file
        with open("/Users/ankuankit/Desktop/pro/MLproject/admin_password.txt", 'w') as f:
            f.write(f"Admin Password Generated: {secure_password}\n")
            f.write("⚠️ DELETE THIS FILE AFTER SAVING PASSWORD SECURELY\n")
        
        print("📁 Password saved to admin_password.txt")
        print("🔒 DELETE admin_password.txt AFTER SAVING PASSWORD!")
        
    else:
        admin_user = User.objects.get(username='admin')
        print("Admin user already exists!")
        print("⚠️  SECURITY WARNING:")
        print("This script may use insecure hardcoded passwords.")
        print("Consider running secure_admin_creation.py for better security.")
        
        # Check if current password is weak
        if admin_user.check_password('admin123') or admin_user.check_password('password'):
            print("🔒 Weak password detected! Generating new secure password...")
            new_password = generate_secure_password()
            admin_user.set_password(new_password)
            admin_user.save()
            
            print("✅ Password updated with secure version!")
            print(f"New Secure Password: {new_password}")

if __name__ == '__main__':
    print("🔐 Admin Creation Script")
    print("⚠️  This script has been modified for security")
    print("🔒 For production, use secure_admin_creation.py")
    print("=" * 50)
    
    create_admin_with_secure_password()
