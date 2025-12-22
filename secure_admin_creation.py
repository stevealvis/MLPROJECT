#!/usr/bin/env python3
"""
Secure Admin User Creation Script
Creates admin users with strong, randomly generated credentials
"""

import os
import sys
import django
import secrets
import string
from django.contrib.auth.models import User
from django.db import IntegrityError

# Setup Django environment
sys.path.append('/Users/ankuankit/Desktop/pro/MLproject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'disease_prediction.settings')
django.setup()

def generate_strong_password(length=16):
    """Generate a strong random password"""
    # Define character sets
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Ensure at least one character from each set
    password = [
        secrets.choice(uppercase),
        secrets.choice(lowercase),
        secrets.choice(digits),
        secrets.choice(special)
    ]
    
    # Fill the rest randomly
    all_chars = uppercase + lowercase + digits + special
    for _ in range(length - 4):
        password.append(secrets.choice(all_chars))
    
    # Shuffle and convert to string
    secrets.SystemRandom().shuffle(password)
    return ''.join(password)

def generate_username():
    """Generate a unique username"""
    prefix = "admin"
    while True:
        # Generate random alphanumeric suffix
        suffix = ''.join(secrets.choice(string.ascii_lowercase + string.digits) 
                        for _ in range(8))
        username = f"{prefix}_{suffix}"
        
        # Check if username already exists
        if not User.objects.filter(username=username).exists():
            return username

def create_secure_admin():
    """Create admin user with secure credentials"""
    try:
        # Generate secure credentials
        username = generate_username()
        password = generate_strong_password(16)
        email = "admin@secure-portal.com"
        
        # Create superuser
        admin_user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        # Display secure credentials
        print("=" * 60)
        print("🔒 SECURE ADMIN USER CREATED SUCCESSFULLY")
        print("=" * 60)
        print(f"Username: {username}")
        print(f"Password: {password}")
        print(f"Email: {email}")
        print("=" * 60)
        print("⚠️  IMPORTANT SECURITY NOTES:")
        print("• Save these credentials securely")
        print("• Change the password after first login")
        print("• Use environment variables in production")
        print("• Enable 2FA for additional security")
        print("=" * 60)
        
        # Save credentials to file (optional)
        credentials_file = "/Users/ankuankit/Desktop/pro/MLproject/admin_credentials.txt"
        with open(credentials_file, 'w') as f:
            f.write(f"SECURE ADMIN CREDENTIALS\n")
            f.write(f"Generated: {django.utils.timezone.now()}\n")
            f.write(f"Username: {username}\n")
            f.write(f"Password: {password}\n")
            f.write(f"Email: {email}\n")
            f.write(f"\n⚠️  DELETE THIS FILE AFTER SAVING CREDENTIALS SECURELY\n")
        
        print(f"📝 Credentials also saved to: {credentials_file}")
        print("🔒 DELETE THIS FILE AFTER SAVING CREDENTIALS!")
        
        return True
        
    except IntegrityError as e:
        print(f"❌ Error: Username already exists - {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def update_existing_admin_passwords():
    """Update any existing admin users with weak passwords"""
    print("\n🔍 Checking existing admin users...")
    
    admin_users = User.objects.filter(is_superuser=True)
    
    if not admin_users.exists():
        print("No admin users found.")
        return
    
    for admin in admin_users:
        print(f"\nAdmin user found: {admin.username}")
        
        # Check if password is weak (this is a simple check)
        if admin.check_password('admin123') or admin.check_password('password') or admin.check_password('123456'):
            print(f"⚠️  Weak password detected for {admin.username}")
            
            # Generate new strong password
            new_password = generate_strong_password(16)
            admin.set_password(new_password)
            admin.save()
            
            print(f"✅ Password updated for {admin.username}")
            print(f"New Password: {new_password}")
            
            # Save updated credentials
            with open("/Users/ankuankit/Desktop/pro/MLproject/admin_credentials_updated.txt", 'a') as f:
                f.write(f"Updated Admin: {admin.username}\n")
                f.write(f"New Password: {new_password}\n")
                f.write(f"Updated: {django.utils.timezone.now()}\n\n")
        else:
            print(f"✅ Password appears secure for {admin.username}")

if __name__ == "__main__":
    print("🔒 Medical Portal - Secure Admin Creation")
    print("=" * 50)
    
    # Create new secure admin
    success = create_secure_admin()
    
    if success:
        # Update existing admin passwords
        update_existing_admin_passwords()
        
        print("\n🎉 Admin setup completed successfully!")
        print("📋 Next steps:")
        print("1. Save the credentials securely")
        print("2. Login with the new admin account")
        print("3. Change the password")
        print("4. Enable 2FA if available")
        print("5. Delete the credentials file")
    else:
        print("\n❌ Admin creation failed. Please check the errors above.")
