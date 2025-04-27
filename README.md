# Health Information System

A comprehensive health information system for managing clients and health programs/services. This Django-based application enables healthcare providers to register clients, create health programs, enroll clients in programs, and access client information through an intuitive user interface and API.

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
![Dashboard Preview](https://media-hosting.imagekit.io/c201dcaf2f974e3e/dashboard.png?Expires=1840391723&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=uBvgWb1h2dMZ5oKM8SMQNrx1cJOlGtP1YvaA5x~pmWLy27pr1CQGZlx9WUMMSbuwd6rvHeWrhcTlTKCI3oBQvLSBcXKUwv9YwMyD3ZjNrlyKFLHVRPmsIInhhslKhY4vdQTv3kfT5ABYkWWaI4icNiOGsIYL7U8mWXZUIdwy~r6R44e9GRWccwacwGymbO3I58ITxQJokqH5ZSYrR7YlBI-Xu5pt301pszgKsEykfxsmdj0deLj6eoi06XbSVGME86Y75jAUfVxWHUgz~hKHFbtWsYKnIn2C~vYTu9va7oGlpIGVM4xhxEvWeOQwO-ldTKmJlPlCrq-~-9ijrpx7ZQ__)


### Health program
![Health program Preview](https://media-hosting.imagekit.io/7ae440a6f28d4239/healthprogram.png?Expires=1840391877&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=2hu0LBpNSBvELRGE322MvAxUXzin6k0RLIeDBROj4RdxM5ec481ocbGVVZZ3EAkT7a8DBUVGC5LxSMYN2uYGV0FW6UP2q4TEIHfXd4RT7jL2ODVW6kIfxO3moXM2l2nTMV2aB60~iTTzSjFPOwpvHN~RjmtShYH09lGJjgs7tj0dzcfwnqt2KLTV-8xzxLA~Qwlh2TB79AgJw9U2WGqQUvXr2IFRoymF6sUw~2WWGkdFWgMd8yhFChe0TN65BIUn8v9AnWz-ogh8IZsbmznFb4uEzdLFTzFqL9pYIMUpe6NOf72yAfTG2bgbjKTct9N-OPb4DqVdvtDx2iHQcshsYQ__)
![Program Detail](https://media-hosting.imagekit.io/a97e0db1f83548a8/programdetails.png?Expires=1840391741&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=H9DNqaHIizMoIvNaYxMFktls4-zQOdLTduWUz-6bjNHi81ivuL0uVlE6KjMnGh9jdvEeTpCGs6~lI5ZVkBUaIuRrW6V6ymdYgHhyLGzIGkbBk-uH1k3As51CoQ3l6RAsbeoG0kXzco83Xz~E1~HOGezQKUkCfbnQO5Hh5455GZbxJe1oKWeZiIFHCHlPqneMZEsynm9X0qlAvc18MLWUiGVs8qHZGavZtJUAw0fg7jwaYikt-Zd785eABYIFk5x95wtn0qgzAUT4Qa2FK3cjgXtoYTD9ipMbdqredMMkhksCzxaHN12Vqbh9JG7ghrDupQElhWIh5LxJzKecC0PsfA__)

### Client Management
![Client List](https://media-hosting.imagekit.io/23038c261fac40e0/clientlist.png?Expires=1840391770&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=tuv5BCUi2yCr39zK3k~-0dtI0ilFOinNoSNPiMlMBv-T5Pu4YrHlLgFsD1h49vOG-5cQn8O0dryYDKV47J3zouDkSBMbcE3vM--ByeFfbLjfacoYkxgO-Ie9Pthe6xcvCJWJL3l7QDuCpmqFMmgJil7eehDmSb3Py7snDn8i~VUFdW3hY8xyASzoGTeSx7DyKO~h71oPPOchawWst8OXOTzkfgsLL5UeuTG8IN7Pcbcfn1j0fYWtUznrIpRTTFUjAqlbMvDBO2-qVd6BhX-1koKs8ynM0Qoj5k3BF2G7392jAfKcZIGN99vjkbFd9pMplUFZHQNpyM83UWKjpTKe0Q__)
![Client Detail](https://media-hosting.imagekit.io/dafa64440d994bc3/clientdetail.png?Expires=1840391755&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=BRgU-ct2nPISeoO3lSbnUvo0qRsxVoks4m2kl64zsEM~f-qZ8w0dbipqb5HQro1WvTxrvQMzw9MelkrqLewusv9wlyV3t6a3g0Sa-hnPbU4madpuKOYoZLC656jkTnbH~DkSAz3hiNAAmTw19bdrdKHCjx4sIDYXIpZqjPdRxP0VJIqckIlt4bmIkHk0keO2JdGhcsS85f~EzhukxaMlF-QnEW3V94ySu0nSZd5to-UOaE~oQtqYnoGn1CzWbIDRDOaWKcwWqB7AZrOjN5uTEicxKIBYTEqUL2TOxE7mfbiVPBP9XSX6BKzs94Zumx9jqwRGrgzDGvSK7zC5hj-yRQ__)


### Program Enrollment
![Enrollment](https://media-hosting.imagekit.io/41ee2c0242a34990/Enrollment.png?Expires=1840391799&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=URugN~ynoHi6Gl7f-2yCcg0ld-u2QIc475sZqz35qIO8PCAI95lvQ1q72lfW5Vd9lQlfGq4TNSCUqNlIFwEHA9v~M3faMWkSn3~vqIFh4kYitDcUnasrwVuegATHSft29vUoukU5dzMSOX3I-I37sMCH0Cyy6W5prYTNNYPwpOKQuMYNdkidvqvU6ycWuBd0j-hKnzc-m9IcFBhbFsQM7U065~a6jZrYsLQBilaSnJk7M8VTf9iidKoSvv5mZYrTGMDDcFOjRZn~MuAIhzYIvjVzhOP2llHUICNYtQmSxObjyzxtZpF0av4aNWu2iYoFgdbEZQO5V-f1n5Oxtrg6Ug__)
![Quick Enrollment](https://media-hosting.imagekit.io/542bc69acc304ec9/quickenrollment.png?Expires=1840391811&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=O5OcoOM2qSD6abeIHdyPiwktbbwZYjC3SakssA5BhWcXJuZI9FSv1t-GFWCKqfeHy-eAPNjNy1880LGfItrTqjlR18CmiDZqDaKDsuzgiuQF74~WY896VTTDtVy1eVQUTqTYH0zYTvXxn-kuLv0XiMkE6jmLRT1Wl03fodKEDqQCeZYjo5~wPoV2yLExi89zSPT2Pgo32OcMCAcNOwrpO3zgYdgO5x0QpYhOtQ8IMuHYSgTGuCHetBZvNEgFTF88XnsJAUggPxUTmD5ypB7pmrqxt0wKZ1Yd~MZuBiuSD7R-4HeMO4nM10uvP6d9KwzZchTgwkH7c62KeH-GogSy4A__)
![Program Enrollment](https://media-hosting.imagekit.io/42bb4346afb54e75/enrollprogram.png?Expires=1840391831&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=JlRJfoyQX6LMKLqfNqKlpJISzcwpfm1qiI1-IiAkIPd57h52~x30yroc3UnmdwQhYwwr48gdxkGx3naDMtspDbORkCRjo9KuIn9-pCIuz6pU3eaCT-AcaWiecqahqoy56sCBXpGmEMG~0UERZJMzFM4w0rCPxklIDTLqQ-Kv1V1MoEJqeqEYzCiLg8iayekNk487M0UR6iFQG0Pnib33DQTv3T2g8khF9MN-Yew6-V~hv7jyi~AZYwTWLkMi3ExJ9EHgZAoURijPKfSre1P7o4Y03HeLnLU6XzB6xu8HICrUDrzBVFXKJ24kkhZtJmIysTAotIhbdJTSd26zdQf6cQ__)

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