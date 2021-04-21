## How to run (on Linux)

```
# Cloning repository
git clone https://github.com/erayerturk/django-rest-api.git
cd django-rest-api

# Installing virtualenv
sudo apt-get install python3-venv
sudo apt install virtualenv

# Creating virtual environment
python3 -m venv venv
source venv/bin/activate

# Installing dependecies
pip3 install -r requirements.txt

# Creating DB
python manage.py makemigrations
python manage.py migrate

# Creating a super user (for 'Sex' field > Male: 0, Female: 1)
python manage.py createsuperuser

# Running cron for notes' alarm
python manage.py crontab add

# Running application
python manage.py runserver
```

## Cron job commands

```
python manage.py crontab add
python manage.py crontab show
python manage.py crontab remove
```

## Documentation

http://localhost:8000/api/v1/docs