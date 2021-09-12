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

*create .env file and add to them SECRET_KEY and DEBUG of your project*
```bash
SECRET_KEY=h5c(wc=n#_za^i9m2# # replace
DEBUG=True # you can replace
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
