Django Social Media Clone 

<h1>Features</h1>

<p>Django backend of social media clone</p>

- Register/Login/Logout/Change password
- Your personnal profile with all your post and profile picture 
- Post about your journey 
- Join group and post in it 

<h1>Installation</h1>

Change directory to blog_backend and setup a virtual environment:

```
python3 -m venv venv 
```

and activate it:

```
source venv/bin/activate
```

Install the dependencies using pip:

```
pip3 install -r requirements.txt
```

Then migrate and create a super user:

```
python3 manage.py makemigrations 
python3 manage.py migrate
python3 manage.py createsuperuser
```

Finally you should be able to start your server by running:

```
python3 manage.py runserver
```

the backend is now running on http://127.0.0.1:8000 !

<h1>Goal</h1>

This application was for learning purpose with Django and Python. 

<h1>To do </h1>

- Frontend
- Notification system
