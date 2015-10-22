import requests

CLIENT_ID = "dAhCaXVVvRdCjh7BcA"
CLIENT_SECRET = "JvuwZv9NPgV6E5MqzW8Lfb3FgjLpNFzK"

REPO_UUID = ""

def get_auth_url():
    return "https://bitbucket.org/site/oauth2/authorize?client_id={0}&response_type=code".format(CLIENT_ID)

def is_logged_in():
    try:
        with open("bitbucket_access_token") as f:
            ACCESS_TOKEN = f.read()
            
        return True
    except:
        return False
    
def get_auth_token(request):
    #headers = {"Content-type": "application/x-www-form-urlencoded"}
    code = request.GET["code"]
    
    data = {"code":code, "grant_type":"authorization_code"}
    auth = (CLIENT_ID, CLIENT_SECRET)
    r = requests.post("https://bitbucket.org/site/oauth2/access_token", data=data, auth=auth)
    
    ACCESS_TOKEN = r.json()["access_token"]
    with open('bitbucket_access_token', 'w') as f:
        f.write(ACCESS_TOKEN)
        
    print ACCESS_TOKEN
    return r.json()
    
def verify(request):

    # ensure we have a session state and the state value is the same as what microsoft returned
    if 'code' not in request.GET:
        return False
    else:
        return True


def get_request_headers():
    with open("bitbucket_access_token") as f:
        ACCESS_TOKEN = f.read()
        
    headers = {"Authorization": "Bearer " + ACCESS_TOKEN}
    return headers
    
def set_repo_uuid(request):
    REPO_UUID = request.GET["repo_uuid"]
    
    # Also save to file. This should reset each time you visit a new repo
    with open("repo_uuid", 'w') as f:
        f.write(REPO_UUID)
        

def get_repo_uuid():
    with open("repo_uuid") as f:
        UUID = f.read()
    return UUID

    
def add_to_wiki(pages_list):
    content = "\n".join(pages_list)
    data = {"content": content }
    
    print "Adding to Wiki"
    try:
        r = requests.post("https://bitbucket.org/api/1.0/repositories/{1}/{0}/wiki/notes".format(get_repo_uuid(), "{}"), data=data)
        print r.reason
    except:
        print "Oops"
        
    if r.ok:
        print "Added to Wiki!!"
        return True
    else: return False