from django.http import HttpResponseRedirect
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
    return HttpResponse("facebook data came")
  else:
    print "facebook login hit"
  return HttpResponseRedirect(reverse('homePage'))

