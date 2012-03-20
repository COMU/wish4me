import cgi, urllib, json, urllib2, oauth, httplib, re
from django.template.context import RequestContext
from facebook.models import FacebookProfile
from django.shortcuts import render_to_response
from contact_importer.utils import *

def home(request):
    user_friends = facebook_contact_import(request)
    return render_to_response('contact_importer/home.html',
                              { 'response': user_friends, },
                                context_instance=RequestContext(request))
