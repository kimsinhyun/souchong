from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponse
import pymongo
import pandas
import urllib
# Create your views here.

def index(request):
    
    return HttpResponse("Hello, world. You're at the polls index.")

def detail(request, question_id):
    return HttpResponse(f"{question_id} detail")

def results(request, question_id):
    return HttpResponse(f"{question_id} results")

def vote(request, question_id):
    return HttpResponse(f"{question_id} vote")
