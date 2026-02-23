# Event Manager - Django Basics Regular Exam

This project is a comprehensive event management system developed for the Django Basics Regular Exam at SoftUni. It provides full CRUD functionality for events and venues, with a responsive and dark-themed UI.

## Project Requirements Met

- **Django version**: Latest stable (>= 5.0.0).
- **Architecture**: 3 distinct Django apps: `events`, `venues`, and `categories`.
- **Database**: PostgreSQL (mandatory).
- **Models**:
  - `Event`: Includes Many-to-One (Venue) and Many-to-Many (Category) relationships.
  - `Venue`: Stores location and capacity.
  - `Category`: Categorization for events.
- **Forms**:
  - `EventForm` (Creation)
  - `EventEditForm` (Editing with read-only timestamp field)
  - `VenueForm` (Venue management)
- **Validation**: Strict model and form validations with user-friendly error messages.
- **Templates**: 11 pages + 1 base template (exceeding the min 10). Includes:
  - Custom 404 page.
  - 8 pages displaying dynamic data from the database.
  - Full CRUD implementation for both Events and Venues.
- **Styling**: Modern dark design using Bootstrap 5 and custom CSS.
- **Documentation**: Well-structured README with setup instructions.

---

## Setup Instructions

### 1. Prerequisites

- Python 3.x installed.
- PostgreSQL server running.

### 2. Environment Setup

Clone the repository and navigate into it:

```bash
# Clone and enter directory
cd EventManagerDjango
```

Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

### 4. Database Configuration

Create the PostgreSQL database and user:

```sql
CREATE DATABASE event_manager_db;
CREATE USER ivan WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE event_manager_db TO ivan;
```

> [!IMPORTANT]
> Ensure your local PostgreSQL configuration matches the credentials in `settings.py`.

### 5. Initialize the Project

Apply migrations and create a superuser:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run the Application

Start the development server:

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser.

## Features

- **Dashboard**: Quick view of upcoming events, top venues, and categories.
- **Event Filtering**: Search by title/description and filter by venue or category.
- **Sorting**: Sort events by date, title, or price.
- **CRUD Operations**: Complete management for events and venues with confirmation steps for deletion.
- **Responsive Design**: Works seamlessly on mobile and desktop.

---

_Developed by Alex Dimitrov_
