from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from elasticsearch import Elasticsearch
from app.models import *
import uuid, os, base64, time
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import datetime
import base64
import os

es = Elasticsearch([{'host': "localhost", 'port': 9200}])

@api_view(['GET', 'POST'])
def user_login(request):
    token = ""
    if request.method == 'POST':
        data = request.data
        for field in ['name', 'uid', 'email', 'profile']:
            if field not in data:
                return HttpResponse("Add " + field)
        uid = str(data['uid'])
        name = data['name']
        email = data['email']
        profile = data['profile']

        try:
            user = User.objects.get(username=uid)
        except User.DoesNotExist:
            user = User.objects.create_user(username=uid)
            user_details =  UserDetails(user=user, reg_id=uid, name=name, email=email, profile=profile)
            user_details.save()
        token = Token.objects.get(user=user)
        token = token.key

    return JsonResponse({"token": token})

@api_view(['GET', 'POST'])
def addproduct(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            data = request.data
            for field in ['title', 'description', 'rent', 'deposit', 'negotiable_flag', 'images', 'location', 'category']:
                if field not in data:
                    return HttpResponse("Add " + field)
                if field == 'location':
                    if 'lat' not in data['location'] and 'long' not in data['location']:
                            return HttpResponse("Add " + field)

            user = UserDetails.objects.get(user = request.user)
            user_id = user.reg_id
            product_id = uuid.uuid4().hex
            images = upload_image(data['images'])
            for i in range(len(images)):
               images[i] = images[i].replace('/home/ubuntu/rr/rr/static/', 'http://54.165.42.145:8001/')
            product_data = {
                "reg_id": user_id,
                "location": [{
                    "lat": float(data['location']['lat']),
                    "lon": float(data['location']['long'])
                    }],
                "title": data['title'],
                "description": data['description'],
                "product_id": product_id,
                "rent": int(data['rent']),
                "deposit": int(data['deposit']),
                "category": data['category'],
                "images": images,
                "negotiable_flag": False,
                "date": str(datetime.date.today())
            }
            es.index(index="rr_products", doc_type="list", id=product_id, body=product_data)
            return Response(product_data)
        else:
            return HttpResponse("User is not Authenticated")


def upload_image(data):
    url = []
    for img in data:
        img = img.encode('UTF-8')
        imagedata =  base64.decodestring(img)
        if not os.path.exists(os.getcwd() + '/static/'):
            os.mkdir(os.getcwd() + '/static/')
        if not os.path.exists(os.getcwd() + '/static/rrimages/'):
            os.mkdir(os.getcwd() + '/static/rrimages/')
        filename = os.getcwd() + '/static/rrimages/' + str(uuid.uuid4().hex) + '.jpg'
        with open(filename, 'wb') as f:
            f.write(imagedata)
        url.append(filename)
    return url

@api_view(['POST', 'GET'])
def product_detail(request):
    if request.method == 'GET':
        data = request.GET.dict()
    else:
        data = request.data
    if not request.user.is_authenticated():
        return HttpResponse("user is not authenticated")
    if 'product_id' not in data:
        return HttpResponse("need Product id")

    query = {"query": {
                     "match": {
                         "product_id":  data["product_id"]
                     }
                 }
            }
    try :         
        result = es.search(index='rr_products', body=query)
        return Response(result['hits']['hits'][0]['_source'])
    except IndexError: 
        return Response({'product_id': 'Invalid product_id'})

def get_query(data):
    if "lat" in data and "lon" in data:
        query = {
                "query": {},
                 "sort": [{
                     "_geo_distance":  {
                         "location": {
                             "lat": data['lat'],
                             "lon": data['lon']
                        },
                        "order": "asc",
                        "unit": "km",
                        "distance_type": "plane"
                    }
                }]
            }
    else:
        query={}

    if "category" in data and query:
        query['query'] = {
                         "match": {
                             "category":  data["category"]
                         }
                     }

    elif 'q' in data and query:
        query['query']={
                       "query": {
                           "multi_match": {
                               "query": data['q'],
                               "fields": ["category", "description", "name"]
                           }
                        }
                    }
    return query

@api_view(['GET', 'POST'])
def get_all_user_product(request):
    if request.method == 'GET':
        data = request.GET.dict()
    else:
        data = request.data     
    query = {"size" : 50,}
    if not  request.user.is_authenticated():
        return HttpResponse("User is not Authenticated")
    if 'reg_id' not in data:
        data['reg_id'] = request.user.username
    if request.user.username != data['reg_id']:
        return JsonResponse({"reg_id": "use your own reg_id"})

    query = {"query": {
                     "match": {
                         "reg_id":  data["reg_id"]
                     }
                 }
            }
    result = es.search(index='rr_products', body=query)
    return Response({'data': get_result(result)})


@api_view(['GET', 'POST'])
def get_all_product(request):
    if request.method=='GET':
        data = request.GET.dict()
    else:
        data = request.data
               
    query = get_query(data)
    result = es.search(index='rr_products', body=query)     
    return Response({'data': get_result(result)})

def get_result(data):
    result = []
    for d in data['hits']['hits']:
        result.append(d['_source'])
    return result
