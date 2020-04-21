from django.shortcuts import render
import urllib
import urllib.request as req
import urllib.error
import re
import random
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict

from Apps.FunnyService.models import jokes
# Create your views here.
def getFunny(request):
    pageIndex = 1
    stories = []
    try:
        url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        headers = {'User-Agent' :user_agent}
        requestInfo = req.Request(url, headers=headers)
        responseInfo = req.urlopen(requestInfo)
        pageCode = responseInfo.read().decode('utf-8')

        if not pageCode:
            print("page load error")
            return JsonResponse({"status": "404", "msg": "don't have stories."}, charset='utf-8')

        pattern = re.compile('h2>(.*?)</h2.*?content">(.*?)</.*?number">(.*?)</', re.S)
        items = re.findall(pattern, pageCode)
        pageStories = []
        for item in items:
            pageStories.append([item[0].strip(), item[1].strip(), item[2].strip()])

        if pageStories:
            stories.append(pageStories)

        if len(stories) > 0:
            pageStories = stories[0]
            pageIndex = random.randint(1, len(pageStories)-1)
            return JsonResponse({"status": "200", "data": pageStories[pageIndex][1],
                                 "name": pageStories[pageIndex][0]}, json_dumps_params={'ensure_ascii': False})
    except urllib.error.URLError as e:
        if hasattr(e, "reason"):
            print("error", e.reason)
            return JsonResponse({"status": "400", "msg": "server break down."}, charset='utf-8')


def saveJoke(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        # 已经存在数据修改，否则创建新的对象
        if jokes.objects.filter(name=name).exists():
            joke = jokes.objects.get(name=name )
            joke.content = request.POST.get('content')
            joke.save()
            # 另外一种方式
            # jokes.objects.filter(name='xxx').update(content='xxxxx')
        else:
            joke = jokes(name=name, content=request.POST.get('content'))
            joke.save()
            # 另外一种方式
            # jokes.objects.create(name='xxxx',content='xxxxx')
        data = {
            'status' : '200',
            'msg' : 'save success'
        }
        return JsonResponse(data=data)
    else:
        data = {
            'status': '401',
            'msg': 'method error'
        }
        return JsonResponse(data=data)


def delJoke(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        # 删除name=name的数据
        joke = jokes.objects.get(name=name)
        joke.delete()
        # 另外一种方式
        # jokes.objects.filter(name='xxxx').delete()
        data = {
            'status': '200',
            'msg': 'delete success'
        }
        return JsonResponse(data=data)
    else:
        data = {
            'status': '401',
            'msg': 'method error'
        }
        return JsonResponse(data=data)


def delAllJoke(request):
    if request.method == 'POST':
        # 删除所有数据
        jokes.objects.all().delete()
        data = {
            'status': '200',
            'msg': 'delete all success'
        }
        return JsonResponse(data=data)
    else:
        data = {
            'status': '401',
            'msg': 'method error'
        }
        return JsonResponse(data=data)


def queryJoke(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        # 根据name查找joke
        joke = jokes.objects.get(name=name)
        if joke:
            data = {
                'status': '200',
                'msg': 'query success',
                'data': model_to_dict(joke)
            }
            return JsonResponse(data=data)
        data = {
            'status': '200',
            'msg': 'query null',
        }
        return JsonResponse(data=data)
    else:
        data = {
            'status': '401',
            'msg': 'method error'
        }
        return JsonResponse(data=data)

def queryAllJoke(request):
    if request.method == 'GET':
        # 根据name查找joke
        querySet = jokes.objects.all()
        jokeList = []
        for i in querySet:
            jokeList.append(model_to_dict(i))
        if jokeList:
            data = {
                'status': '200',
                'msg': 'query success',
                'data': jokeList
            }
            return JsonResponse(data=data)
        data = {
            'status': '200',
            'msg': 'query null',
        }
        return JsonResponse(data=data)
    else:
        data = {
            'status': '401',
            'msg': 'method error'
        }
        return JsonResponse(data=data)