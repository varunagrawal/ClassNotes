from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

import onenote

# Create your views here.
def index(request):
    return render(request, 'index.html')
    
def sign_in(request):
    print "Redirecting user"
    
    redirect_to = "https://login.live.com/oauth20_authorize.srf?client_id={0}&scope=wl.basic%20office.onenote_create%20office.onenote&response_type=code&redirect_uri={1}".format(onenote.CLIENT_ID, onenote.REDIRECT_URI)
    return HttpResponseRedirect(redirect_to)
    
def signed_in(request):
    if onenote.verify(request):
    
        data = onenote.get_auth_token(request)

        return HttpResponseRedirect("/notes/notebooks")
    
    else: return HttpResponse("Please provide permission to ClassNotes.\n {0}".format(request)) 
    
def notebooks(request):
    notebooks = onenote.get_notebooks()
    context = {'notebooks': notebooks}
    #print notebooks["value"]
    
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
    #return HttpResponse(str(pages))    
    return render(request, 'pages.html', context)
    
    # write the pages to the repository Wiki and stay on the page
    
    # code to write to wiki
    
    #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    
def page(request):
    page = onenote.get_page_content(request.GET["id"])
    
    #context = { 'page': page }
    #return render(request, 'page.html', context)
    return HttpResponse(str(page))
    