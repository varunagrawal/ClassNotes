from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

import onenote
import bitbucket

# sample repo_uuid = 3d316876-a913-4b20-b183-d57e919f96dc

BASE_URL = "https://afternoon-waters-2404.herokuapp.com"
# DEV_URL = "https://classnotes-varunagrawal.c9.io"


# Create your views here.
def index(request):
    bitbucket_login_url = "{0}/notes/atlas_signin".format(BASE_URL)
    microsoft_login_url = "{0}/notes/ms_signin".format(BASE_URL)

    repo_uuid = None
    if "repo_uuid" in request.GET:
        repo_uuid = request.GET["repo_uuid"]
        # bitbucket_login = bitbucket.is_logged_in(repo_uuid)
        # bitbucket.set_repo_uuid(repo_uuid)
        
        # response = render(request, 'index.html?bitbucket_login={0}'.format(bitbucket_login))
        return HttpResponse(repo_uuid)

    need_ms_signin = onenote.get_auth_token(request) is None
    need_atlassian_signin = not bitbucket.is_logged_in(repo_uuid)

    context = {'bitbucket_login': bitbucket_login_url, 'need_atlassian_signin': need_atlassian_signin,
               'microsoft_login': microsoft_login_url, 'need_ms_signin': need_ms_signin}

    response = render(request, 'index.html', context)
    response.set_cookie('repo_uuid', repo_uuid)
    return response
    
    
def ms_sign_in(request):
    print("Redirecting user")
    
    redirect_to = "https://login.live.com/oauth20_authorize.srf?client_id={0}&scope=wl.basic%20office.onenote_create%20office.onenote&response_type=code&redirect_uri={1}".format(onenote.CLIENT_ID, onenote.REDIRECT_URI)
    return HttpResponseRedirect(redirect_to)
    
    
def ms_signed_in(request):
    if onenote.verify(request):
    
        data = onenote.get_auth_token(request)

        return HttpResponseRedirect("/notes/notebooks")
    
    else:
        return HttpResponse("Please provide permission to ClassNotes.\n {0}".format(request))


def atlas_sign_in(request):
    print("Bitbucket Sign in")
    return HttpResponseRedirect(bitbucket.get_auth_url())


def atlas_signed_in(request):
    if bitbucket.verify(request): 
        print("getting token")
        bitbucket.get_auth_token(request)
        print("got token")
        
        return HttpResponseRedirect("/notes?bitbucket_login=1")
        
    else:
        return HttpResponse("Please grant access to Bitbucket, {0}".format(request.GET))
    
    
def notebooks(request):
    
    if 'repo_uuid' in request.COOKIES:
        repo_uuid = request.COOKIES['repo_uuid']
    
    books = onenote.get_notebooks(repo_uuid)
    context = {'notebooks': books}
    # print(notebooks
    
    return render(request, 'notebooks.html', context)#("List of Notebooks\n{0}".format(str(notebooks)))


def sections(request):
    if 'repo_uuid' in request.COOKIES:
        repo_uuid = request.COOKIES['repo_uuid']
    
    sections = onenote.get_sections(request.GET["id"], request.GET["name"], repo_uuid)
    context = {'sections': sections}
    
    # return HttpResponse(sections["value"])
    return render(request, 'sections.html', context)


def pages(request):
    if 'repo_uuid' in request.COOKIES:
        repo_uuid = request.COOKIES['repo_uuid']
    
    pages = onenote.get_pages(request.GET["id"], request.GET["name"], repo_uuid)
    context = {'pages': pages}
    # print(request.GET["name"]
    
    # write the pages to the repository Wiki and stay on the page
    if not bitbucket.is_logged_in(repo_uuid):
        return HttpResponseRedirect("/notes")
    
    # code to write to wiki
    page_links_md = onenote.get_page_links_md(pages)
    
    bitbucket.add_to_wiki(page_links_md, repo_uuid)
    
    # return HttpResponse(str(pages))
    return render(request, 'pages.html', context)
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    
def page(request):
    repo_uuid = None
    if 'repo_uuid' in request.COOKIES:
        repo_uuid = request.COOKIES['repo_uuid']
    
    page = onenote.get_page_content(request.GET["id"], repo_uuid)
    
    # context = { 'page': page }
    # return render(request, 'page.html', context)
    return HttpResponse(str(page))
