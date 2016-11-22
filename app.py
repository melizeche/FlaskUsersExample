import sqlite3
import bcrypt
from flask import Flask, request, render_template, Response
from flask import g  # for app context

app = Flask(__name__)

DB = 'db.sqlite'

# DATABASE STUFF
def get_db():
    db = getattr(g, '_database', None)  # if there's no db in context
    if db is None:
        db = g._database = sqlite3.connect(DB)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')
# END DATABASE STUFF

def insert_user(dname, demail, dpassword):
    # Hash a password for the first time, with a randomly-generated salt
    hashed = bcrypt.hashpw(dpassword.encode('utf-8'), bcrypt.gensalt())
    db = get_db()
    query = "INSERT into user (name,email,password) VALUES ('%s','%s','%s')" % (
        dname, demail, hashed.decode('utf-8'))
    print(query)
    result = db.execute(query)
    db.commit() # TODO: Catch unique email exeption
    return True


def check_login(demail, dpassword):
    db = get_db()
    query = "select email, password from user where email='%s'" % (demail)
    cursor = db.execute(query) # Execute Query
    row = cursor.fetchone()
    if(row):  # Checks if the query returned something(not None)
        email, password = row
        if demail == email: # Checks email and password(hashed with bcrypt)
            if bcrypt.checkpw(dpassword.encode('utf-8'), password.encode('utf-8')):
                return True # Yay!
    return False

# ROUTES/VIEWS
@app.route('/')
def index():
    # Simple response
    return 'Hello, World!'
    # 'Proper' response
    #return Response("Hello, World!", status=200, mimetype="text/html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            if(email and password):  # if the values aren't empty
                if(check_login(email, password)):
                    return "LOGIN OK", 200
                else:
                    return "LOGIN FAIL", 403
            return email
        except Exception as e:
            print(e)
            return '{"error":"incomplete or bad arguments"}', 400
    elif request.method == 'GET':
        return render_template("login.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    print(request.method)
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            if(name and email and password):  # if the values aren't empty
                insert_user(name, email, password)
                return "User created", 201
            return Response('{"error":"All fields are mandatory"}', status=400,
                                mimetype='application/json')
        except Exception as e:
            print(e)
            return '{"error":"incomplete or bad arguments"}', 400
    else:
        print(request.args)
        # for GET parameters -> email = request.args.get('email')
    return Response(render_template("register.html"), status=200)


if __name__ == "__main__":
    app.run()
