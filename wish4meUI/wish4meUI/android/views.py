from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def facebook_login(request):
  if request.POST:
    print "post request"
    facebookID = request.POST['id']
    print "id = " + facebookID
    facebookEmail = request.POST['email']
    print "email = " + facebookEmail
    response =  HttpResponse("facebook data came", content_type="text/plain")
    print "response is \n", response
    return response
  else:
    print "facebook login hit"
  return HttpResponseRedirect(reverse('homePage'))

