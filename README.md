# Custom Admin Base

A base toolkit for building a Django-Suit compatible Admin theme.

## Installation

```bash
pip install django-custom-admin-base
```

### settings.py

This app should come before other admin style modifiers, since it replaces admin/base.html and admin/base_site.html

```python
INSTALLED_APPS = [
    "...",
    "custom_admin",
    "your_app_to_extend_custom_admin",
    "...",
    "django.contrib.admin",
]
```

Migrations and Static files

```bash
manage.py migrate custom_admin
manage.py collectstatic
```
