#!/bin/bash
# Railway Deployment Script for Admin Fix
# This script should be run after deploying to Railway

echo "🚀 Railway Deployment Script"
echo "=============================================="

# Navigate to the app directory (Railway uses /app)
cd /app 2>/dev/null || cd "$(dirname "$0")"

echo "📋 Step 1: Running Django migrations..."
python manage.py migrate --run-syncdb

echo "📋 Step 2: Collecting static files..."
python manage.py collectstatic --noinput

echo "📋 Step 3: Creating admin user..."
python manage.py create_admin_user --force || python railway_admin_fix.py

echo "📋 Step 4: Running diagnostic check..."
python railway_admin_fix.py

echo "✅ Deployment completed!"
echo ""
echo "🔐 Admin Login Credentials:"
echo "   URL: https://skinpro.up.railway.app/accounts/sign_in_admin"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "🔧 Django Admin (alternative):"
echo "   URL: https://skinpro.up.railway.app/admin/"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "⚠️  IMPORTANT: Change the default password after first login!"
echo ""
echo "🌐 Site URL: https://skinpro.up.railway.app"
echo "📖 For detailed instructions, see RAILWAY_DEPLOYMENT_FIX_PLAN.md"
