from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

import onenote

# Create your views here.
def index(request):
    return HttpResponse("Hi! Welcome to ClassNotes.")
    
def sign_in(request):
    print "Redirecting user"
    
    redirect_to = "https://login.live.com/oauth20_authorize.srf?client_id={0}&scope=wl.basic%20wl.basic&response_type=token&redirect_uri={1}".format(onenote.CLIENT_ID, onenote.REDIRECT_URI)
    return HttpResponseRedirect(redirect_to)
    
def signed_in(request):
    if request.method == "POST":
        print "POST"
        print request.POST#.get('accesss_token')
    elif request.method == "GET":
        print "GET"
        print request.GET
    else: print request
    
    return HttpResponse("success!")