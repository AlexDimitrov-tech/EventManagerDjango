# Event Manager

This is a web app I built using Django and PostgreSQL. The idea is pretty simple — you can manage events, where they happen (venues), and what type of events they are (categories). It supports creating, editing, deleting and filtering all of that.

---

## What it does

- Create and manage events with a title, description, date, time, price and venue
- Assign multiple categories to an event
- Full venue management (name, address, capacity)
- Filter and search events by name, venue or category
- Sort events by date, title or price
- Custom 404 page

---

## Tech stack

- Python 3.12
- Django 6.x
- PostgreSQL
- Bootstrap 5 (just for grid/layout, most styling is custom CSS)

---

## Setup

You'll need Python 3 and PostgreSQL installed before starting.

**1. Clone the repo and go into the folder**

```
git clone <repo-url>
cd event_manager
```

**2. Create a virtual environment**

```
python3 -m venv venv
source venv/bin/activate
```

**3. Install requirements**

```
pip install -r requirements.txt
```

**4. Create the database**

Make sure PostgreSQL is running, then:

```
createdb event_manager_db
```

**5. Edit database settings if needed**

Open `event_manager/settings.py` and update the DATABASES section with your PostgreSQL credentials. By default it expects:
- user: `ivan`
- password: `postgres`
- host: `localhost`
- port: `5432`

**6. Run migrations**

```
python manage.py makemigrations
python manage.py migrate
```

**7. Start the server**

```
python manage.py runserver
```

Then go to `http://127.0.0.1:8000/` in your browser.

---

## Project layout

```
event_manager/
├── event_manager/       <- project config (settings, urls, wsgi)
├── events/              <- events app (models, views, forms, urls, templatetags)
├── venues/              <- venues app
├── categories/          <- categories app
├── templates/           <- all HTML templates
│   ├── base.html
│   ├── 404.html
│   ├── events/
│   ├── venues/
│   └── categories/
├── static/
│   └── css/style.css
├── manage.py
└── requirements.txt
```

---

## Database models

**Event** — title, description, date, time, price (decimal), venue (foreign key), categories (many-to-many)

**Venue** — name, address, capacity (integer), created_at

**Category** — name, description

---

## Notes

- `events/templatetags/` has custom filters for formatting dates, times and prices the way I wanted
- The setup script `setup_db.sh` can be used to create the database and run migrations in one go if you prefer that
- Admin panel is available at `/admin/` if you create a superuser with `python manage.py createsuperuser`

---

Made for a school/course assignment. Not intended for production use.
