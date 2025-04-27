# Health Information System

A comprehensive health information system for managing clients and health programs/services. This Django-based application enables healthcare providers to register clients, create health programs, enroll clients in programs, and access client information through an intuitive user interface and API.

![Dashboard Preview](https://i.imgur.com/z8cGPRQ.png)

## 🌟 Features

- **Client Management**: Register, search, and manage client profiles with detailed information
- **Health Programs**: Create and manage various health programs (TB, Malaria, HIV, etc.)
- **Program Enrollment**: Enroll clients in one or more health programs with tracking capabilities
- **Quick Enrollment**: Fast-track enrollment process from any point in the application
- **Data Visualization**: Interactive charts showing program distribution and enrollment trends
- **Client Search**: Find clients using name, ID, or contact information
- **RESTful API**: Access client and program data via a secure API
- **Responsive Design**: Works seamlessly across desktop, tablet, and mobile devices

## 🚀 Technology Stack

- **Backend**: Django 4.2.7
- **API**: Django REST Framework
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Visualization**: Chart.js
- **Animations**: AOS (Animate On Scroll)
- **Icons**: Font Awesome
- **Database**: SQLite (development), PostgreSQL (production)

## 📋 Project Structure

```
health_info_system/                  # Main project directory
├── manage.py
├── health_info_system/              # Project settings directory
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                            # Core application
│   ├── models.py                    # Database models
│   ├── views.py                     # View functions
│   ├── forms.py                     # Form definitions
│   ├── urls.py                      # URL patterns
│   ├── admin.py                     # Admin configurations
│   └── templates/                   # HTML templates
├── api/                             # API application
│   ├── views.py                     # API view functions
│   └── urls.py                      # API URL patterns
├── static/                          # Static files
└── media/                           # User uploaded files
```

## ⚙️ Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Valentino-Junior/health-information-system.git
   cd health-information-system
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

## 💻 Key Components

### 1. Core Models

The system is built around three main models:

```python
class HealthProgram(models.Model):
    """Model representing a health program (TB, Malaria, HIV, etc.)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Client(models.Model):
    """Model representing a client in the health system"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    programs = models.ManyToManyField(HealthProgram, through='Enrollment')
    # Additional fields...

class Enrollment(models.Model):
    """Model representing a client's enrollment in a health program"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    program = models.ForeignKey(HealthProgram, on_delete=models.CASCADE)
    enrollment_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    # Additional fields...
```

### 2. Key Features Implementation

#### Client Registration
The application provides a user-friendly form for registering new clients with all relevant personal and contact information.

#### Health Program Management
Healthcare administrators can create and manage health programs with detailed descriptions and tracking capabilities.

#### Client Enrollment
The system offers multiple ways to enroll clients in health programs:
- From client details page
- Through quick enrollment feature
- Bulk enrollment capabilities

#### Data Visualization
Interactive charts provide insights into:
- Program distribution (how many clients are enrolled in each program)
- Enrollment trends over time (tracking program growth)

### 3. API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/clients/` | GET | List all clients |
| `/api/clients/{id}/` | GET | Get details for a specific client |
| `/api/clients/{id}/enrollments/` | GET | Get a client's enrolled programs |
| `/api/programs/` | GET | List all health programs |
| `/api/programs/{id}/` | GET | Get details for a specific program |
| `/api/programs/{id}/clients/` | GET | Get clients enrolled in a program |

## 🔐 Security Considerations

- **Authentication**: All sensitive operations require authentication
- **CSRF Protection**: Protection against cross-site request forgery
- **Input Validation**: Thorough validation of all user inputs
- **Secure API**: API endpoints protected with authentication
- **Data Privacy**: Client information is protected and access-controlled

## 📱 Screenshots

### Dashboard
![Dashboard](https://i.imgur.com/z8cGPRQ.png)

### Client Management
![Client List](https://i.imgur.com/dVZsmlv.png)
![Client Detail](https://i.imgur.com/VzNyiF1.png)

### Program Enrollment
![Enrollment](https://i.imgur.com/NB3hfOK.png)
![Quick Enrollment](https://i.imgur.com/YJKFgS2.png)

## 🚀 Deployment

The application can be deployed on:
- Heroku
- AWS Elastic Beanstalk
- DigitalOcean
- PythonAnywhere
- Any platform supporting Django applications

## 🧪 Testing

The project includes tests for:
- Models
- Views
- Forms
- API endpoints

To run tests:
```bash
python manage.py test
```

## 🛠️ Future Improvements

- User role-based access control
- Enhanced reporting capabilities
- SMS notifications for appointments
- Mobile application integration
- Electronic health records integration
- Offline functionality

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Valentine Ochieng - [ojvalentine14@gmail.com](mailto:ojvalentine14@gmail.com)

---

For any questions or support, please [open an issue](https://github.com/Valentino-Junior/health-information-system/issues/new) on GitHub.