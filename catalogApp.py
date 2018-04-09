from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
from flask import Flask, render_template, request, redirect, url_for
from flask import make_response, flash, jsonify, session as login_session
from setupDatabase import Base, Catalog, Item, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random, string
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2
import json
import requests

# Initializes flask app
app = Flask(__name__)

# Reads client_secrets.json file to get client_id value for Google Sign in
CLIENT_ID = json.loads(open('client_secrets.json','r').read())['web']['client_id']

#Create session and connect to DB
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Create a state token to prevent request
#Store it in the session for later validation
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login4.html', STATE=state)
@app.route('/logout')
def logout():
   # remove the username from the session if it is there
    login_session.pop('state', None)
    return render_template('login.html')

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
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
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
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output

# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'],email=login_session[
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
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url,'GET')[0]
    print('result is ')
    print(result)

    if result['status'] != '200':
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# # Login the application using facebook sign in
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print("access token received %s " % access_token)


    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/v2.9/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1].decode('utf-8')
    data = json.loads(result)

    token = result.split(',')[0].split(':')[1].replace('"', '')
    #token = 'access_token=' + data['access_token']
    # see: https://discussions.udacity.com/t/
    #   issues-with-facebook-oauth-access-token/233840?source_topic_id=174342

    # Use token to get user info from API
    # make API call with new token
    url = 'https://graph.facebook.com/v2.9/me?%s&fields=name,id,email,picture' % token

    h = httplib2.Http()
    result = h.request(url, 'GET')[1].decode('utf-8')
    print("url sent for API access:%s"% url)
    print("API JSON result: %s" % result)
    data = json.loads(result)

    login_session['provider'] = 'facebook'
    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['facebook_id'] = data['id']
    login_session['picture'] = data['picture']["data"]["url"]
    login_session['access_token'] = access_token

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output

# Logout the application using facebook sign out
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions' & facebook_id
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1].decode('utf-8')
    return 'you have been logged out'

# Logout depend on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['access_token']
            del login_session['gplus_id']
            del login_session['username']
            del login_session['email']
            del login_session['picture']
            del login_session['provider']
        #if login_session['provider'] == 'facebook':
        #    fbdisconnect()
        #    del login_session['provider']
        #    del login_session['username']
        #    del login_session['email']
        #    del login_session['facebook_id']
        #    del login_session['picture']
        #    del login_session['access_token']
        
        flash("You have successfully been logged out.")
        return redirect(url_for('showCatalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCatalog'))

# JSON APIs to view Information
@app.route('/catalog/JSON')
def catalogJSON():
    catalog = session.query(Catalog).all()
    items=session.query(Item).all()
    return jsonify(Item=[i.serialize for i in items])

@app.route('/catalog/<int:catalog_id>/item/JSON')
def catalogItemJSON(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    items=session.query(Item).filter_by(catalog_id=catalog_id).all()
    return jsonify(Item=[i.serialize for i in items])

#Add your API Endipoint Here
@app.route('/catalog/<int:catalog_id>/item/<int:item_id>/JSON')
def itemJSON(catalog_id, item_id):
    item = session.query(Item).filter_by(id = item_id).one()
    return jsonify(Item = item.serialize)

# Show catalogs
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    catalog = session.query(Catalog).all()
    return render_template('catalog.html',catalog=catalog)

# Crete new catalog
@app.route('/catalog/new/', methods=['GET', 'POST'])
def newCatalog():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCatalog = Catalog(
            name=request.form['name'])
        session.add(newCatalog)
        session.commit()
        flash("New catalog created!")
        return redirect(url_for('showCatalog'))
    else:
         return render_template('newCatalog.html')

# Edit catalog
@app.route('/catalog/<int:catalog_id>/edit/', methods=['GET', 'POST'])
def editCatalog(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if request.form['name']:
            catalog.name = request.form['name']
        session.add(catalog)
        session.commit()
        flash("Catalog has been edited")
        return redirect(url_for('showCatalog'))
    else:
         return render_template(
            'editCatalog.html',catalog_id = catalog_id,catalog=catalog)

# Delete catalog
@app.route('/catalog/<int:catalog_id>/delete/', methods=['GET', 'POST'])
def deleteCatalog(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if catalog.user_id != login_session['user_id']:
        return "<script>function my Function() {alert('You are not authorized to delete this catalog. Please create your own catalog in order to delete.');}</script><bodyonload='myFunction()''>"
    if request.method == 'POST':
        session.delete(catalog)
        session.commit()
        flash("Catalog has been deleted")
        return redirect(url_for('showCatalog'))
    else:
        return render_template('deleteCatalog.html',catalog_id=catalog_id,catalog=catalog)

# Show specific item
@app.route('/catalog/<int:catalog_id>/item/')
def showItem(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    items = session.query(Item).filter_by(catalog_id=catalog.id)
    return render_template('item.html', items=items,catalog=catalog, catalog_id=catalog_id)

# Create new item
@app.route('/catalog/<int:catalog_id>/item/new/', methods=['GET', 'POST'])
def newItem(catalog_id):
    items = session.query(Item).all()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newItems = Item(
            name=request.form['name'],description=request.form['description'],year=request.form['year'], catalog_id=catalog_id)
        session.add(newItems)
        session.commit()
        flash("New item created!")
        return redirect(url_for('showItem', catalog_id=catalog_id,item=items))
    else:
        return render_template('newItem.html',catalog_id=catalog_id,item=items)

# Edit item
@app.route('/catalog/<int:catalog_id>/item/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(catalog_id,item_id):
    itemEdit = session.query(Item).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if request.form['name']:
            itemEdit.name = request.form['name']
        if request.form['description']:
            itemEdit.description = request.form['description']
        if request.form['year']:
            itemEdit.year = request.form['year']
        session.add(itemEdit)
        session.commit()
        flash("Item has been edited")
        return redirect(url_for('showItem', catalog_id=catalog_id))
    else:
        return render_template('editItem.html', catalog_id=catalog_id, item_id=item_id, item=itemEdit)

# Delete item
@app.route('/catalog/<int:catalog_id>/item/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(catalog_id,item_id):
    itemDelete = session.query(Item).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        session.delete(itemDelete)
        session.commit()
        flash("Item has been deleted")
        return redirect(url_for('showItem', catalog_id=catalog_id))
    else:
        return render_template('deleteItem.html',catalog_id=catalog_id, item_id=item_id,item=itemDelete)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 4000)
