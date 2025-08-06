#!/usr/bin/env python3
"""
Setup script for the Task Manager Django project.
This script helps initialize the project and create initial data.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path('.env')
    if not env_file.exists():
        print("📝 Creating .env file...")
        with open(env_file, 'w') as f:
            f.write("""SECRET_KEY=django-insecure-your-secret-key-here-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
""")
        print(" .env file created")
    else:✅
        print(" .env file already exists")✅

def create_superuser():
    """Create a superuser if none exists"""
    try:
        from django.contrib.auth.models import User
        from django.core.management import execute_from_command_line
        
        if not User.objects.filter(is_superuser=True).exists():
            print("👤 Creating superuser...")
            print("Please enter the following information:")
            
            username = input("Username: ").strip()
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            
            if username and password:
                user = User.objects.create_superuser(username, email, password)
                print(f"✅ Superuser '{username}' created successfully")
            else:
                print("❌ Username and password are required")
        else:
            print("✅ Superuser already exists")
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")

def create_sample_data():
    """Create sample categories and tasks"""
    try:
        from django.core.management import execute_from_command_line
        from tasks.models import Category, Task
        from django.contrib.auth.models import User
        
        # Create sample categories
        categories_data = [
            {'name': 'Work', 'color': '#007bff', 'description': 'Work-related tasks'},
            {'name': 'Personal', 'color': '#28a745', 'description': 'Personal tasks'},
            {'name': 'Urgent', 'color': '#dc3545', 'description': 'Urgent tasks'},
            {'name': 'Learning', 'color': '#ffc107', 'description': 'Learning and development tasks'},
        ]
        
        for cat_data in categories_data:
            Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
        
        print(" Sample categories created")
        ✅
        # Create sample tasks if user exists
        user = User.objects.filter(is_superuser=True).first()
        if user:
            tasks_data = [
                {
                    'title': 'Welcome to Task Manager',
                    'description': 'This is your first task. You can edit or delete it.',
                    'status': 'todo',
                    'priority': 'medium',
                    'created_by': user
                },
                {
                    'title': 'Explore the Dashboard',
                    'description': 'Check out the dashboard to see your task statistics.',
                    'status': 'in_progress',
                    'priority': 'high',
                    'created_by': user
                }
            ]
            
            for task_data in tasks_data:
                Task.objects.get_or_create(
                    title=task_data['title'],
                    defaults=task_data
                )
            
            print("✅ Sample tasks created")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")

def main():
    """Main setup function"""
    print("🚀 Setting up Task Manager Django Project")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("❌ Error: manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies. Please check your Python environment.")
        sys.exit(1)
    
    # Run migrations
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        print("❌ Failed to create migrations.")
        sys.exit(1)
    
    if not run_command("python manage.py migrate", "Running migrations"):
        print("❌ Failed to run migrations.")
        sys.exit(1)
    
    # Create superuser
    print("\n👤 Superuser Setup")
    print("You can skip this step by pressing Enter for all fields.")
    create_superuser()
    
    # Create sample data
    print("\n📊 Sample Data")
    create_sample_data()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run the development server: python manage.py runserver")
    print("2. Visit http://127.0.0.1:8000/ to see your application")
    print("3. Visit http://127.0.0.1:8000/admin/ to access the admin interface")
    print("\nHappy coding! 🚀")

if __name__ == "__main__":
    main() 