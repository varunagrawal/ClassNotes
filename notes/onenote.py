import requests
import json
import urllib2
import urllib
import re
from django.conf import settings
from django.core.urlresolvers import reverse


CLIENT_ID = "0000000044169032"
CLIENT_SECRET = "ldaqv85Q8ecpwvltVb4DRlBmLzWPNab7"
REDIRECT_URI = "https://classnotes-varunagrawal.c9.io/notes/signedin"

BASE_URL = "https://www.onenote.com/api/v1.0/me/notes{0}"

def get_request_headers():
    with open("access_token") as f:
        ACCESS_TOKEN = f.read()
        
    headers = {"Authorization": "Bearer " + ACCESS_TOKEN}
    return headers

def get_auth_token(request):
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    code = request.GET["code"]
    
    data = {"client_id": CLIENT_ID, "redirect_uri": REDIRECT_URI, "client_secret": CLIENT_SECRET, "code":code, "grant_type":"authorization_code"}
    r = requests.post("https://login.live.com/oauth20_token.srf", data=data, headers=headers)
    
    ACCESS_TOKEN = r.json()["access_token"]
    with open('onenote_access_token', 'w') as f:
        f.write(ACCESS_TOKEN)
        
    print ACCESS_TOKEN
    return r.json()
    
def verify(request):

    # ensure we have a session state and the state value is the same as what microsoft returned
    if 'code' not in request.GET:
        return False
    else:
        return True
        
def sign_in():
    pass

def get_notebooks():
    headers = get_request_headers()
    r = requests.get(BASE_URL.format("/notebooks"), headers=headers)
    
    return r.json()
    
def get_sections(id, name):
    headers = get_request_headers()
    r = requests.get(BASE_URL.format("/notebooks/{0}/sections".format(id)), headers=headers)
    
    return r.json()
    
def get_pages(id, name):
    headers = get_request_headers()
    r = requests.get(BASE_URL.format("/sections/{0}/pages".format(id)), headers=headers)
    
    return r.json()


def get_page(id):
    headers = get_request_headers()
    r = requests.get(BASE_URL.format("/pages/{0}".format(id)), headers=headers)
    
    return r.json()


def get_page_content(id):
    headers = get_request_headers()
    r = requests.get(BASE_URL.format("/pages/{0}/content?includeIDs=true".format(id)), headers=headers)
    
    return r.text.encode('utf-8')