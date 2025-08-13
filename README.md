# Task Manager - Django Project

A comprehensive task management system built with Django that demonstrates end-to-end web development concepts.

## 🚀 Features

### Core Functionality
- **Task Management**: Create, edit, delete, and track tasks
- **Category Organization**: Organize tasks by categories with color coding
- **Priority Levels**: Set task priorities (Low, Medium, High, Urgent)
- **Status Tracking**: Track task status (To Do, In Progress, Review, Done)
- **Due Date Management**: Set and track due dates with overdue notifications
- **User Assignment**: Assign tasks to different users
- **Comments System**: Add comments to tasks for collaboration
- **Comments System**: Add comments to tasks for collaboration

### User Interface
- **Modern Dashboard**: Beautiful dashboard with statistics and recent tasks
- **Responsive Design**: Mobile-friendly Bootstrap 5 interface
- **Real-time Updates**: AJAX-powered task completion
- **Search & Filter**: Advanced filtering and search capabilities
- **Beautiful UI**: Modern gradient sidebar and card-based layout

### Authentication & Security
- **User Authentication**: Secure login/logout system
- **Permission System**: Users can only access their own tasks
- **Admin Interface**: Full Django admin integration
- **Email Verification**: Optional email verification for new accounts

### API & Integration
- **REST API**: Complete REST API with Django REST Framework
- **JSON Endpoints**: API endpoints for tasks, categories, and comments
- **Authentication**: API authentication and permissions

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7
- **Database**: SQLite (can be easily changed to PostgreSQL/MySQL)
- **Frontend**: Bootstrap 5, Font Awesome, jQuery
- **API**: Django REST Framework
- **Authentication**: Django Allauth
- **Forms**: Django Crispy Forms with Bootstrap 5

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd scmm-main
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

### 8. Access the Application
- **Main Application**: http://127.0.0.1:8000/
- **Admin Interface**: http://127.0.0.1:8000/admin/
- **API Endpoints**: http://127.0.0.1:8000/api/

## 📁 Project Structure

```
scmm-main/
├── taskmanager/              # Main project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── tasks/                   # Tasks app
│   ├── models.py            # Database models
│   ├── views.py             # Views and API endpoints
│   ├── forms.py             # Django forms
│   ├── serializers.py       # REST API serializers
│   ├── admin.py             # Admin interface
│   └── urls.py              # App URL configuration
├── accounts/                # Accounts app
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   └── tasks/               # Task-specific templates
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User-uploaded files
├── requirements.txt         # Python dependencies
└── manage.py               # Django management script
```

## 🎯 Key Learning Concepts

### Django Fundamentals
1. **Models**: Database design with relationships
2. **Views**: Class-based and function-based views
3. **Forms**: Form handling and validation
4. **Templates**: Template inheritance and context
5. **URLs**: URL routing and patterns
6. **Admin**: Custom admin interface

### Advanced Django
1. **Authentication**: User management and permissions
2. **API Development**: REST API with DRF
3. **File Uploads**: Handling file attachments
4. **Search & Filtering**: Advanced querying
5. **AJAX**: Dynamic content updates
6. **Security**: CSRF protection, permissions
### Frontend Development
1. **Bootstrap 5**: Modern responsive design
2. **JavaScript**: Interactive features
3. **CSS**: Custom styling and animations
4. **Responsive Design**: Mobile-first approach


#### 🔧 Configuration

# Environment Variables
Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

### Database Configuration
The project uses SQLite by default. To use PostgreSQL or MySQL, update the database settings in `taskmanager/settings.py`.

## 📚 API Documentation

### Task Endpoints
- `GET /api/tasks/` - List all tasks
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/{id}/` - Get task details
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task
- `POST /api/tasks/{id}/mark_complete/` - Mark task as complete

### Category Endpoints
- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create a new category
- `GET /api/categories/{id}/` - Get category details
- `PUT /api/categories/{id}/` - Update category
- `DELETE /api/categories/{id}/` - Delete category

### Authentication
All API endpoints require authentication. Use session authentication or include credentials in requests.

## 🎨 Customization

### Adding New Features
1. **Models**: Add new fields to existing models or create new models
2. **Views**: Create new views in `tasks/views.py`
3. **Templates**: Add new templates in `templates/tasks/`
4. **URLs**: Add URL patterns in `tasks/urls.py`

### Styling
- Modify CSS in `templates/base.html`
- Add custom styles in the `<style>` section
- Override Bootstrap classes as needed

## 🚀 Deployment

### Production Settings
1. Set `DEBUG = False` in settings
2. Configure a production database (PostgreSQL recommended)
3. Set up static file serving
4. Configure email settings
5. Use environment variables for sensitive data

### Deployment Options
- **Heroku**: Easy deployment with Git integration
- **DigitalOcean**: VPS deployment
- **AWS**: Scalable cloud deployment
- **Docker**: Containerized deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues or have questions:
1. Check the Django documentation
2. Review the code comments
3. Create an issue in the repository

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)
- [Django Allauth](https://django-allauth.readthedocs.io/)

---

**Happy Coding! 🎉** Being able to navigate your way around a product hierarchy and understand the different levels of the structures as well as being able to join these details to sales related datasets will be super valuable for anyone wanting to work within a financial, customer or exploratory analytics capacity.

