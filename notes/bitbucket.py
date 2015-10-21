import requests

CLIENT_ID = "dAhCaXVVvRdCjh7BcA"
CLIENT_SECRET = "JvuwZv9NPgV6E5MqzW8Lfb3FgjLpNFzK"

def get_auth_url():
    return "https://bitbucket.org/site/oauth2/authorize?client_id={0}&response_type=code".format(CLIENT_ID)
    
    
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

    