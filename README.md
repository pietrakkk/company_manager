# Company manager
   
Application yto manage companies.

## Requirements
    virtualenv, python3.6


## Installation
  
Create .env file in config directory (You can use .env.example).  

Setup environment by typing:

```virtualenv venv -p python3.6```

Install dependencies:

```. env/bin/activate && pip install -r requirements.txt```

Run migrations:

```python manage.py migrate```

Add test data:

```python manage.py loaddata fixtures.json```

Start application:

```python manage.py runserver```