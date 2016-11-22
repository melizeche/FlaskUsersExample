# FlaskUsers

Just an Register/Login example in Flask with bcrypt for password hashing

## System requirements
* Python 3.3+
* Virtualenv(Optional)

# Environment requirements
* Flask 0.10+
* bcrypt 3.1+

## Set environment
```
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
```

## Initialize DB
```
export FLASK_APP=app.py
flask initdb
```

## RUN
```
flask run
```
or
```
python app.py
```

## TODO
* Add SQLAlchemy example
* Better documentation
* Proper templates(css and that kind of fancy stuff)
* Catch more exceptions
