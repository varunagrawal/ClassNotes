from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

import onenote
import bitbucket

# Create your views here.
def index(request):
    
    if "repo_uuid" in request.GET:
        bitbucket.set_repo_uuid(request)
    
    return render(request, 'index.html')
    
def ms_sign_in(request):
    print "Redirecting user"
    
    redirect_to = "https://login.live.com/oauth20_authorize.srf?client_id={0}&scope=wl.basic%20office.onenote_create%20office.onenote&response_type=code&redirect_uri={1}".format(onenote.CLIENT_ID, onenote.REDIRECT_URI)
    return HttpResponseRedirect(redirect_to)
    
def ms_signed_in(request):
    if onenote.verify(request):
    
        data = onenote.get_auth_token(request)

        return HttpResponseRedirect("/notes/notebooks")
    
    else: return HttpResponse("Please provide permission to ClassNotes.\n {0}".format(request)) 


def atlas_sign_in(request):
    print "Bitbucket Sign in"
    return HttpResponseRedirect(bitbucket.get_auth_url())

def atlas_signed_in(request):
    if bitbucket.verify(request): 
        bitbucket.get_auth_token(request)
        return HttpResponseRedirect("/notes")
        
    else: return HttpResponse("Please grant access to Bitbucket")
    
def notebooks(request):
    notebooks = onenote.get_notebooks()
    context = {'notebooks': notebooks}
    #print notebooks
    
    return render(request, 'notebooks.html', context)#("List of Notebooks\n{0}".format(str(notebooks)))

def sections(request):
    sections = onenote.get_sections(request.GET["id"], request.GET["name"])
    context = {'sections': sections }
    
    #return HttpResponse(sections["value"])
    return render(request, 'sections.html', context)

def pages(request):
    pages = onenote.get_pages(request.GET["id"], request.GET["name"])
    context = { 'pages': pages }
    #print request.GET["name"]
    
    # write the pages to the repository Wiki and stay on the page
    if not bitbucket.is_logged_in():
        return HttpResponseRedirect("/notes")
    
    # code to write to wiki
    page_links_md = onenote.get_page_links_md(pages)
    
    bitbucket.add_to_wiki(page_links_md)
    
    #return HttpResponse(str(pages))    
    return render(request, 'pages.html', context)
    #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    
def page(request):
    page = onenote.get_page_content(request.GET["id"])
    
    #context = { 'page': page }
    #return render(request, 'page.html', context)
    return HttpResponse(str(page))
    