from django.utils.encoding import smart_str
from django.http import HttpResponse, HttpResponseRedirect

def connect_json(request):
    response = HttpResponse(open('connect.json').read())
    #response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('connect.json')
    #response['X-Sendfile'] = smart_str('../connect.json')
    # It's usually a good idea to set the 'Content-Length' header too.
    # You can also set any other required headers: Cache-Control, etc.
    return response