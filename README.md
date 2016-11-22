# Simple register/login Flask example

## Requirements
* Python 3.3+
* Virtualenv(Optional)

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
