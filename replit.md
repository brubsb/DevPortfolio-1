# Overview

This is a personal portfolio web application built with Flask (Python) that showcases a developer's projects, skills, work experience, and provides a contact form. The application is designed as a single-page portfolio with multiple sections including hero/landing area, projects showcase, skills display, experience timeline, and contact functionality. The frontend uses Bootstrap 5 with custom CSS for responsive design and modern animations, while the backend handles data management and form submissions using SQLAlchemy ORM.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Architecture
- **Framework**: Flask (Python) with SQLAlchemy ORM for database operations
- **Database**: SQLite by default with PostgreSQL support via environment configuration
- **Models**: Four main entities - Project, Skill, Experience, and Contact
- **Forms**: Flask-WTF for form validation with Portuguese language validation messages
- **Session Management**: Flask sessions with configurable secret key via environment variables
- **Deployment Ready**: Configured with ProxyFix middleware for production deployment

## Frontend Architecture  
- **Template Engine**: Jinja2 templates with base template inheritance
- **CSS Framework**: Bootstrap 5 for responsive grid and components
- **Styling**: Custom CSS with CSS variables for theming (dark blue theme)
- **JavaScript**: Vanilla JavaScript for interactivity with AOS (Animate On Scroll) library
- **Animation**: Custom particle effects, scroll animations, and hover interactions
- **Icons**: Font Awesome for iconography
- **Responsive Design**: Mobile-first approach with breakpoint-specific optimizations

## Data Architecture
- **Projects**: Title, description, technologies, GitHub/live URLs, categorization, and featured status
- **Skills**: Name, category (frontend/backend/tools), proficiency levels (1-100), and custom ordering
- **Experience**: Company details, positions, date ranges, and priority ordering
- **Contact**: Form submissions storage with name, email, subject, and message fields

## File Structure
- **app.py**: Application factory and configuration
- **models.py**: SQLAlchemy database models
- **routes.py**: URL endpoints and request handlers
- **forms.py**: WTForms form definitions with validation
- **templates/**: Jinja2 HTML templates
- **static/**: CSS, JavaScript, and asset files

# External Dependencies

## Python Packages
- **Flask**: Web framework for backend API and routing
- **Flask-SQLAlchemy**: Database ORM for data persistence
- **Flask-WTF**: Form handling and CSRF protection
- **WTForms**: Form validation library
- **Werkzeug**: WSGI utilities including ProxyFix middleware

## Frontend Libraries
- **Bootstrap 5**: CSS framework from CDN for responsive components
- **Font Awesome 6**: Icon library from CDN for UI elements
- **AOS (Animate On Scroll)**: Animation library from CDN for scroll-triggered effects

## Database
- **SQLite**: Default development database (file-based)
- **PostgreSQL**: Production database support via DATABASE_URL environment variable

## Configuration
- **Environment Variables**: SESSION_SECRET for security, DATABASE_URL for database connection
- **Logging**: Python logging configured for debugging
- **Production Ready**: ProxyFix middleware for reverse proxy deployment