# Job Board Platform

A modern job board application built with Django that connects job seekers with employers. This platform allows users to browse job listings, submit applications, and manage their job search process efficiently.

## 🚀 Features

### For Job Seekers
- Browse available job listings
- Search jobs by title, location, and category
- Create and manage user profiles
- Submit job applications with resume and cover letter
- Track application status
- Save favorite jobs

### For Employers/Admins
- Post and manage job listings
- Review applications
- Manage job categories
- Track application statistics
- User management

## 🛠️ Technologies Used

- **Backend:** Django 5.1.6
- **Frontend:** Bootstrap 5
- **Database:** SQLite
- **Authentication:** Django Authentication System
- **API:** Django REST Framework
- **Documentation:** drf-yasg (Swagger/OpenAPI)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/job-board.git
   cd job-board
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Visit the application**
   - Main site: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## 🗂️ Project Structure

```
job_board/
├── jobs/                   # Main application directory
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # URL configurations
│   └── admin.py           # Admin interface setup
├── templates/             # HTML templates
│   └── jobs/
│       ├── base.html
│       ├── home.html
│       ├── auth/
│       └── dashboard/
├── static/               # Static files (CSS, JS, images)
├── media/               # User-uploaded files
└── manage.py           # Django management script
```

## 👥 User Roles

1. **Anonymous Users**
   - View job listings
   - Search jobs
   - Register/Login

2. **Registered Users**
   - Apply for jobs
   - Track applications
   - Manage profile
   - Upload resume/CV

3. **Admin Users**
   - Manage job listings
   - Review applications
   - Manage categories
   - User management

## 🔒 Authentication

- User registration with email verification
- Login with username/password
- Password reset functionality
- Admin authentication for dashboard access

## 📝 API Documentation

Access the API documentation at:
- Swagger UI: http://127.0.0.1:8000/swagger/
- ReDoc: http://127.0.0.1:8000/redoc/

## 💼 Available Endpoints

- `/` - Home page
- `/user-login/` - User login
- `/user-signup/` - User registration
- `/user-dashboard/` - User dashboard
- `/admin-dashboard/` - Admin dashboard
- `/apply-job/<job_id>/` - Job application form
- `/search-jobs/` - Job search

## 🔍 Search Functionality

Users can search jobs by:
- Job title
- Location
- Category
- Employment type
- Salary range
- Experience level

## 📤 Application Process

1. User selects a job
2. Fills application form with:
   - Personal information
   - Professional details
   - Resume upload
   - Cover letter
   - Additional links (LinkedIn, Portfolio)
3. Submits application
4. Tracks status in dashboard

## 🛡️ Security Features

- CSRF protection
- Password hashing
- File upload validation
- User authentication
- Permission-based access control

## 🔄 Future Improvements

- [ ] Email notifications
- [ ] Advanced search filters
- [ ] Company profiles
- [ ] Application analytics
- [ ] Mobile app integration
- [ ] Social media integration

## 👥 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

Your Name - your.email@example.com
Project Link: https://github.com/yourusername/job-board

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap Team
- Font Awesome
- All contributors and testers 