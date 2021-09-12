# DEMO - API

Demo project to start rest api

## Create Virtual env
```bash
python -m venv env
```


## Activate Virtual env
```bash
source env/bin/activate
```


## Install dev dependencies
```bash
pip install -r requirements-dev.txt
```

## Install prod dependencies
```bash
pip install -r requirements.txt
```


### Migrate database
```bash
python manage.py migrate
```


### Create super user
```bash
python manage.py createsuperuser
```


### Start the app in development mode
```bash
python manage.py runserver
```
