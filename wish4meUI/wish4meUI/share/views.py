from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from wish4meUI.wish.models import Wish

def home(request):
    return HttpResponseRedirect('/')

def show(request, wish_id):
   wish = get_object_or_404(Wish, pk=wish_id)
   return render_to_response('share/show.html', {'wish': wish}, context_instance=RequestContext(request))
