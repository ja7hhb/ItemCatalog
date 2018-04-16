# Item Catalog Web App
URL: https://catalogitem00.herokuapp.com/

This is a project for udacity nanodegree program.

This is RESTful web application about philosophy catalog item using Flask which accesss a SQL database.  To createauthentication system, this project has OAuth2.


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

## JSON Endpoints
The following are open to the public:

Catalog JSON: `/catalog/JSON` - Displays the whole catalog.

Category Items JSON: `/catalog/<string:catalogname>/item/JSON` - Displays items for a specific catalog

Category Item JSON: `/catalog/<string:catalogname>/item/<string:itemname>/JSON`- Displays a specific catalog item.
