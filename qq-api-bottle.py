from pyoauth2 import Client
import json
import bottle

# To autoreload after saving changes
bottle.run(reloader=True)

CLIENT_ID = 'ENTER_YOUR_CLIENT_ID'
CLIENT_SECRET = 'ENTER_YOUR_CLIENT_SECRET'
REDIRECT_URL = "https://login.qqcatalyst.com/WinformCallback/completed.htm"
AUTHORIZE_URL = "https://login.qqcatalyst.com/oauth/authorize"
ACCESS_TOKEN_URL = "https://login.qqcatalyst.com/oauth/token"
RESOURCE_URL = "https://api.qqcatalyst.com"
userName = 'ENTER_YOUR_USERNAME'
password = 'ENTER_YOUR_PASSWORD'
ind = 2

client = Client(CLIENT_ID, CLIENT_SECRET, site=RESOURCE_URL, authorize_url=AUTHORIZE_URL, token_url=ACCESS_TOKEN_URL)

access_token = client.password.get_token(userName, password, redirect_uri=REDIRECT_URL)

@bottle.route('/')
def index():
    res = access_token.get('/Lookups.svc/LoginStatus')
    bottle.response.content_type = 'application/json'
    return json.dumps(res.parsed, indent=ind, sort_keys=True)

@bottle.route('/customers/<kwd>')
def customers(kwd):
    res = access_token.get('/Contacts.svc/Customer?keyword=' + kwd)
    bottle.response.content_type = 'application/json'
    return json.dumps(res.parsed, indent=ind, sort_keys=True)

@bottle.route('/customer/<cid>')
def customer(cid):
    res = access_token.get('/Contacts.svc/Customer/' + cid)
    bottle.response.content_type = 'application/json'
    return json.dumps(res.parsed, indent=ind, sort_keys=True)

@bottle.route('/policies/<cid>')
def policies(cid):
    res = access_token.get('/Policies.svc/Policy?customerid=' + cid)
    bottle.response.content_type = 'application/json'
    return json.dumps(res.parsed, indent=ind, sort_keys=True)

@bottle.route('/policy/<pid>')
def policy(pid):
    res = access_token.get('/Policies.svc/Policy/' + pid)
    bottle.response.content_type = 'application/json'
    return json.dumps(res.parsed, indent=ind, sort_keys=True)

@bottle.route('/bydate/<start>/<end>')
def bydate(start, end):
    res = access_token.get('/Policies.svc/PoliciesByDateModifiedCreated?startDate='+start+'&endDate='+end)
    bottle.response.content_type = 'application/json'
    return json.dumps(res.parsed, indent=ind, sort_keys=True)

@bottle.route('/ctypes')
def ctypes():
    res = access_token.get('/Lookups.svc/ContactTypes')
    bottle.response.content_type = 'application/json'
    return json.dumps(res.parsed, indent=ind, sort_keys=True)

@bottle.route('/csubtypes')
def csubtypes():
    res = access_token.get('/Lookups.svc/ContactSubTypes')
    bottle.response.content_type = 'application/json'
    return json.dumps(res.parsed, indent=ind, sort_keys=True)


@bottle.route('/ctypes_sub')
def ctypes_sub():
    res = access_token.get('/Lookups.svc/ContactTypesAndSubTypes')
    bottle.response.content_type = 'application/json'
    return json.dumps(res.parsed, indent=ind, sort_keys=True)


@bottle.error(404)
def error404(error):
    return '404, Nothing here, sorry'

bottle.run(host='0.0.0.0', port=80)
