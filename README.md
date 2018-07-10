# Item Catalog Web App
URL: https://catalogitem00.herokuapp.com/

This is a project for <a href="https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004"> Udacity Full Stack Web Developer Nanodegree</a>.

This is RESTful web application about philosophy catalog item using Flask which accesss a SQL database.  To create authentication system, this project has OAuth2 with Google API.

<img src="https://github.com/ja7hhb/ItemCatalog/blob/image/static/img/Screen%20Shot%202018-07-10%20at%204.49.43%20PM.png" alt="Smiley face" height="100%" width="100%">

If user login, receive grant to change web content.

<img src="https://github.com/ja7hhb/ItemCatalog/blob/image/static/img/Screen%20Shot%202018-07-10%20at%204.56.20%20PM.png" height="100%" width="100%">

## requirements

Vagrant

Virtual Box

python3

flask

## step
clone this repo: `git clone https://github.com/ja7hhb/ItemCatalog.git`

move ItemCatalog directory: `cd ItemCatalog`

create virtual environment: `vagrant up`&`vagrant ssh`

move vagrant directory: `cd /vagrant`

run catalogApp.py: `python3 catalogApp.py`

Go to http://localhost:5000/ in your browser: `http://localhost:5000/`

## JSON Endpoints
The following are open to the public:

Catalog JSON: `/catalog/JSON` - Displays the whole catalog.

Category Items JSON: `/catalog/<string:catalogname>/item/JSON` - Displays items for a specific catalog

Category Item JSON: `/catalog/<string:catalogname>/item/<string:itemname>/JSON`- Displays a specific catalog item.
