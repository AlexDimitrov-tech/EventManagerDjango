# Event Manager

A Django web application for managing events, venues, and categories.

## Features

- Full CRUD operations for Events and Venues
- Event filtering and sorting
- Category management
- Responsive Bootstrap design
- Custom template filters and tags

## Requirements

- Python 3.8+
- PostgreSQL
- Django 5.0+

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd event_manager
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL database:
```bash
createdb event_manager_db
```

5. Update database settings in `event_manager/settings.py` if needed:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'event_manager_db',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

6. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

7. Create a superuser (optional, for admin access):
```bash
python manage.py createsuperuser
```

8. Run the development server:
```bash
python manage.py runserver
```

9. Open your browser and navigate to `http://127.0.0.1:8000/`

## Project Structure

```
event_manager/
├── event_manager/          # Main project directory
│   ├── settings.py         # Project settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── events/                 # Events app
│   ├── models.py          # Event model
│   ├── views.py           # Event views
│   ├── forms.py           # Event forms
│   ├── urls.py            # Event URLs
│   └── templatetags/      # Custom template tags
├── venues/                 # Venues app
│   ├── models.py          # Venue model
│   ├── views.py           # Venue views
│   ├── forms.py           # Venue forms
│   └── urls.py            # Venue URLs
├── categories/             # Categories app
│   ├── models.py          # Category model
│   ├── views.py           # Category views
│   └── urls.py            # Category URLs
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── 404.html           # Custom 404 page
│   ├── events/            # Event templates
│   ├── venues/            # Venue templates
│   └── categories/        # Category templates
└── manage.py              # Django management script
```

## Database Models

- **Event**: Main event model with title, description, date, time, venue (FK), categories (M2M), and price
- **Venue**: Venue model with name, address, and capacity
- **Category**: Category model with name and description

## Environment Variables

For local development, update the database credentials in `event_manager/settings.py`:

- `NAME`: Database name (default: 'event_manager_db')
- `USER`: PostgreSQL user (default: 'postgres')
- `PASSWORD`: PostgreSQL password (default: 'postgres')
- `HOST`: Database host (default: 'localhost')
- `PORT`: Database port (default: '5432')

## Usage

1. Navigate to the home page to see upcoming events
2. Use the navigation menu to access Events, Venues, and Categories
3. Create, edit, and delete events and venues
4. Filter events by venue, category, or search term
5. Sort events by date, title, or price

## License

This project is created for educational purposes.

