# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render
from django.views.decorators import csrf
from KB_query import query_main as query

import json

def index(request):
    return render(request, 'index.html')
def d3rdf(request):
    return render(request, 'd3rdf.html')
def search(request):
    Dict={}
    List=[]
    q1=''
    if request.POST:
        q1=request.POST['q']
        List = query.query_function(q1)
    return render(request, "kbqa.html", {'List': json.dumps(List)})
    #return HttpResponse(json.dumps({"status": status,"result": result }))