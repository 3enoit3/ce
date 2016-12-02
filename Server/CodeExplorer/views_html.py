
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import Context, loader
from django.http import Http404

from .models import ceNodes, ceEdges

def index(request):
    aNodes = ceNodes.objects.all()
    aContext = Context({'ceNodes': aNodes})

    aTemplate = loader.get_template('index.html')

    return HttpResponse(aTemplate.render(aContext))

