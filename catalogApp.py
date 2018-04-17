from http.server import HTTPServer, BaseHTTPRequestHandler
from flask import Flask, render_template, request, redirect, url_for
from flask import make_response, flash, jsonify, session as login_session
from setupDatabase import Base, Catalog, Item, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
import string
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2
import json
import requests

# Initializes flask app
app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.debug = True

# Reads client_secrets.json file to get client_id value for Google Sign in
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Create session and connect to DB
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create a state token to prevent request
# Store it in the session for later validation
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Log in the application using google sign in
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    req = h.request(url, 'GET')[1]
    req_json = req.decode('utf8').replace("'", '"')
    result = json.loads(req_json)
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    # See if user exists, if it doesn't make a new one
    try:
        user_id = getUserID(login_session['email'])
    except:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: \
    150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
        'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user.id


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Logout the application using google sign out
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)

    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCatalog'))
    else:
        response = make_response(json.dumps(
            'Failed to disconnect', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view Information
@app.route('/catalog/JSON')
def catalogJSON():
    catalog = session.query(Catalog).all()
    items = session.query(Item).all()
    return jsonify(Item=[i.serialize for i in items])


@app.route('/catalog/<string:catalogname>/item/JSON')
def catalogItemJSON(catalogname):
    catalog = session.query(Catalog).filter_by(catalogname=catalogname).one()
    items = session.query(Item).filter_by(
        catalogname=catalog.catalogname).all()
    return jsonify(Item=[i.serialize for i in items])


# Add your API Endipoint Here
@app.route('/catalog/<string:catalogname>/item/<string:itemname>/JSON')
def itemJSON(catalogname, itemname):
    item = session.query(Item).filter_by(itemname=itemname).one()
    return jsonify(Item=item.serialize)


# Show catalogs
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    catalog = session.query(Catalog).all()
    return render_template('catalog.html', catalog=catalog)


# Crete new catalog
@app.route('/catalog/new/', methods=['GET', 'POST'])
def newCatalog():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCatalog = Catalog(
            catalogname=request.form['name'])
        session.add(newCatalog)
        session.commit()
        flash("New catalog created!")
        return redirect(url_for('showCatalog'))
    else:
        return render_template('newCatalog.html')


# Edit catalog
@app.route('/catalog/<string:catalogname>/edit/', methods=['GET', 'POST'])
def editCatalog(catalogname):
    if 'username' not in login_session:
        return redirect('/login')
    catalog = session.query(Catalog).filter_by(catalogname=catalogname).one()
    if catalog.user_id != login_session['user_id']:
        response = make_response(
            json.dumps("Can't edit this because you're not this catalog owner"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if request.method == 'POST':
        if request.form['name']:
            catalog.catalogname = request.form['name']
        session.add(catalog)
        session.commit()
        flash("Catalog has been edited")
        return redirect(url_for('showCatalog'))
    else:
        return render_template(
            'editCatalog.html', catalogname=catalogname, catalog=catalog)


# Delete catalog
@app.route('/catalog/<string:catalogname>/delete/', methods=['GET', 'POST'])
def deleteCatalog(catalogname):
    if 'username' not in login_session:
        return redirect('/login')
    catalog = session.query(Catalog).filter_by(catalogname=catalogname).one()
    if catalog.user_id != login_session['user_id']:
        response = make_response(
            json.dumps("Can't delete this because you're not this catalog owner"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if request.method == 'POST':
        session.delete(catalog)
        session.commit()
        flash("Catalog has been deleted")
        return redirect(url_for('showCatalog'))
    else:
        return render_template(
            'deleteCatalog.html', name=catalogname, catalog=catalog)


# Show specific item
@app.route('/catalog/<string:catalogname>/item/')
def showItem(catalogname):
    catalog = session.query(Catalog).filter_by(catalogname=catalogname).one()
    item = session.query(Item).filter_by(catalogname=catalog.catalogname)
    return render_template(
        'item.html', item=item, catalog=catalog, catalogname=catalogname)


# Create new item
@app.route('/catalog/<string:catalogname>/item/new/', methods=['GET', 'POST'])
def newItem(catalogname):
    if 'username' not in login_session:
        return redirect('/login')
    item = session.query(Item).all()
    if request.method == 'POST':
        newItems = Item(
            itemname=request.form['name'],
            description=request.form['description'],
            year=request.form['year'], catalogname=catalogname)
        session.add(newItems)
        session.commit()
        flash("New item created!")
        return redirect(url_for(
            'showItem', catalogname=catalogname, item=item))
    else:
        return render_template(
            'newItem.html', catalogname=catalogname, item=item)


# Edit item
@app.route('/catalog/<string:catalogname>/item/<string:itemname>/edit/',
           methods=['GET', 'POST'])
def editItem(catalogname, itemname):
    if 'username' not in login_session:
        return redirect('/login')
    item = session.query(Item).filter_by(itemname=itemname).one()
    if item.user_id != login_session['user_id']:
        response = make_response(
            json.dumps("Can't edit this because you're not this item owner"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['year']:
            item.year = request.form['year']
        session.add(item)
        session.commit()
        flash("Item has been edited")
        return redirect(url_for('showItem', catalogname=catalogname))
    else:
        return render_template('editItem.html', catalogname=catalogname,
                               itemname=itemname, item=item)


# Delete item
@app.route('/catalog/<string:catalogname>/item/<string:itemname>/delete/',
           methods=['GET', 'POST'])
def deleteItem(catalogname, itemname):
    if 'username' not in login_session:
        return redirect('/login')
    item = session.query(Item).filter_by(itemname=itemname).one()
    if item.user_id != login_session['user_id']:
        response = make_response(
            json.dumps("Can't delete this because you're not this catalog owner"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Item has been deleted")
        return redirect(url_for('showItem', catalogname=catalogname))
    else:
        return render_template('deleteItem.html', catalogname=catalogname,
                               itemname=itemname, item=item)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
