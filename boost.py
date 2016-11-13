from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

import hashlib, json
from os import urandom
app = Flask(__name__)

# Set up server connections
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://super:uP,up&AWAY0@127.0.0.1/boost'
db = SQLAlchemy(app)

# Helper Functions
def generate_api_key():
    return urandom(64).encode("hex")

def hash_password(password):
    return str(hashlib.sha512(password).hexdigest())

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))
    api_key = db.Column(db.String(64))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = hash_password(password)

    def check_api_key(self, submitted_key):
        return self.api_key == submitted_key

class Org(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org_name = db.Column(db.String(50), unique=True)
    short_description = db.Column(db.String(250))
    long_description = db.Column(db.Text)
    icon_url = db.Column(db.String(250))

    def __init__(self, org_name, short_description, description, icon_url):
        self.org_name = org_name
        self.short_description = short_description
        self.description = description
        self.icon_url = icon_url

# API Routing
@app.route('/')
def index():
    return "Index for Boost"

@app.route('/register', methods=['POST'])
def register():
    form_email = request.form['email']
    form_user = request.form['username']
    form_pass = request.form['password']

    app.logger.debug("email: " + form_email)
    app.logger.debug("username: " + form_user)
    app.logger.debug("password: " + form_pass)

    user_check = User.query.filter_by(username=form_user).first()
    email_check = User.query.filter_by(email=form_email).first()

    if user_check is not None or email_check is not None:
        abort(406)
    
    new_user = User(form_email, form_user, form_pass)
    db.session.add(new_user)
    db.session.commit()

    # Return 200 or some HTTP success code
    message = {
            'message': 'Successful',
    }
    resp = jsonify(message)
    resp.status_code = 201

    return resp
    

@app.route('/login', methods=['POST'])
def login():
    # Authenticate username and password
    form_email = request.form['email']
    form_pass = request.form['password']
    password_hash = hash_password(form_pass)
    user = User.query.filter_by(email=form_email).first()

    if user is None:
        abort(401)

    if str(user.password) != password_hash:
        abort(401)

    app.logger.debug(user.email)
    app.logger.debug(str(user.password))
    
    # Generate API Key and Update DB
    api_key = generate_api_key()
    user.api_key = api_key
    db.session.commit()

    # Return userid and API key to user
    json_data = {'uid':user.id, 'api_key':user.api_key}
    resp = jsonify(**json_data)
    resp.status_code = 200
    return resp

@app.route('/organization/', defaults={'org_id': None})
@app.route('/organization/<int:org_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def organization(org_id):
    if request.method == "GET":
        return oraganization_get(org_id)
    elif request.method == "POST":
        return organization_post(request)
    elif request.method == "PUT":
        return organization_put(request)
    else:
        return organization_delete(request)

def oraganization_get(org_id):
    # CHeck if org_id has been set
    if org_id is not None:
        org = Org.query.filter_by(id = org_id).first()

        if org is None:
            abort(404)

        json_data = {
            'id':org.id,
            'org_name':org.org_name,
            'short_description':org.short_description,
            'long_description':org.long_description,
            'icon_url':org.icon_url
        }
        
        resp = jsonify(**json_data)
        resp.status_code = 200
        return resp

    else:
        # If not set get all
        organizations = Org.query.order_by(Org.id)

        json_data = []

        for i, org in enumerate(organizations):
            json_data.append({
                'id':org.id, 
                'org_name':org.org_name,
                'short_description':org.short_description,
                'long_description':org.long_description,
                'icon_url':org.icon_url
                })
        resp = json.dumps(json_data)
        return resp

def organization_post(request):
    return None

def organization_put(requet):
    return None

def organization_delete(requset):
    return None

@app.route('/payment', methods=['GET', 'POST', 'PUT', 'DELETE'])
def payment():
    return None

# GET, POST, PUT, DELETE Functions for /payment 
# Make sure to pass request params and session info
def payment_get():
    return None

def payment_post():
    return None

def payment_put():
    return None

def payment_delete():
    return None

@app.route('/donate/', methods=['GET', 'POST'])
def donate():
    return None

# GET, POST, PUT, DELETE Functions for /payment 
# Make sure to pass request params and session info
def donate_get():
    return None

def donate_post():
    return None

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("80"), debug=True)
