import requests
import json
import urllib2
import urllib
import re
from django.conf import settings
from django.core.urlresolvers import reverse
import utils

CLIENT_ID = "0000000044169032"
CLIENT_SECRET = "ldaqv85Q8ecpwvltVb4DRlBmLzWPNab7"
#REDIRECT_URI = "https://classnotes-varunagrawal.c9.io/notes/ms_signedin" #
REDIRECT_URI = "https://afternoon-waters-2404.herokuapp.com/notes/ms_signedin" #"https://classnotes-varunagrawal.c9.io/notes/ms_signedin"

BASE_URL = "https://www.onenote.com/api/v1.0/me/notes{0}"

ONENOTE_ACCESS_TOKEN_FILE = "onenote_access_token"

def get_request_headers(repo_uuid):
    
    ACCESS_TOKEN = utils.get_token(repo_uuid, "OneNote")
    #with open(ONENOTE_ACCESS_TOKEN_FILE) as f:
    #    ACCESS_TOKEN = f.read()
        
    headers = {"Authorization": "Bearer " + ACCESS_TOKEN}
    return headers

def get_auth_token(request):
    
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    code = request.GET["code"]
    
    data = {"client_id": CLIENT_ID, "redirect_uri": REDIRECT_URI, "client_secret": CLIENT_SECRET, "code":code, "grant_type":"authorization_code"}
    r = requests.post("https://login.live.com/oauth20_token.srf", data=data, headers=headers)
    
    ACCESS_TOKEN = r.json()["access_token"]
    
    if request.COOKIES.has_key( 'repo_uuid' ):
        repo_uuid = request.COOKIES[ 'repo_uuid' ]
    
    utils.add_onenote_token_to_db(repo_uuid, ACCESS_TOKEN)
    
    #with open(ONENOTE_ACCESS_TOKEN_FILE, 'w') as f:
    #    f.write(ACCESS_TOKEN)
        
    #print ACCESS_TOKEN
    return r.json()
    
def verify(request):

    # ensure we have a session state and the state value is the same as what microsoft returned
    if 'code' not in request.GET:
        return False
    else:
        return True
        
def sign_in():
    pass

def get_notebooks(repo_uuid):
    headers = get_request_headers(repo_uuid)
    r = requests.get(BASE_URL.format("/notebooks"), headers=headers)
    
    print "got notebooks"
    
    return r.json()
    
def get_sections(id, name, repo_uuid):
    headers = get_request_headers(repo_uuid)
    r = requests.get(BASE_URL.format("/notebooks/{0}/sections".format(id)), headers=headers)
    
    return r.json()
    
def get_pages(id, name, repo_uuid):
    headers = get_request_headers(repo_uuid)
    r = requests.get(BASE_URL.format("/sections/{0}/pages".format(id)), headers=headers)
    
    return r.json()


def get_page(id, repo_uuid):
    headers = get_request_headers(repo_uuid)
    r = requests.get(BASE_URL.format("/pages/{0}".format(id)), headers=headers)
    
    return r.json()


def get_page_content(id, repo_uuid):
    headers = get_request_headers(repo_uuid)
    r = requests.get(BASE_URL.format("/pages/{0}/content".format(id)), headers=headers)
    
    return r.text.encode('utf-8')
    
def get_page_links_md(pages):
    all_pages = pages["value"]
    pages_md = []
    
    for page in all_pages:
        s = "* [{0}]({1})".format(page["title"], page["links"]["oneNoteWebUrl"]["href"])
        pages_md.append(s)
    
    return pages_md
    