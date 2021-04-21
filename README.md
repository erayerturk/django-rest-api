## How to run

```
cd django-rest-api
pip3 install virtualenv 
virtualenv venv
source venv/bin/activate

pip3 install -r requirements.txt
python manage.py create superuser # to create an admin account
python manage.py crontab add
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