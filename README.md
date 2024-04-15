# Flask-Todolist

Simple-Flask-Todolist is a To Do List web application with the most basic
features of most web apps, i.e. accounts/login

## Explore
Try it out!

### Manually
If you prefer to run it directly on your local machine using
[venv](https://docs.python.org/3/library/venv.html).

    pip install -r requirements.txt
    FLASK_APP=todolist.py
    flask db upgrade
    flask run

## Extensions
In the process of this project I used a couple of extensions.

Usage               | Flask-Extension
------------------- | -----------------------
Model & ORM         | [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/latest/)
Migration           | [Flaks-Migrate](http://flask-migrate.readthedocs.io/en/latest/)
Forms               | [Flask-WTF](https://flask-wtf.readthedocs.org/en/latest/)
Login               | [Flask-Login](https://flask-login.readthedocs.org/en/latest/)

I tried out some more, but for the scope of this endeavor the above mentioned extensions sufficed.
