from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from .models import *
from .main import *

query_context = []
"""
接受参数：request
返回： 展示主页面
"""
def home(request):
    global query_context
    query_context = main()
    return render(request, 'GoAbroad/home.html')


"""
接受参数：request
返回： 展示所有的在数据库的信息
"""
def list(request):
    global query_context
    query_context = main()
    news = News.objects.all()
    abs = []
    for item in news:
        abs.append(item.text[0:20])
    length = len(news)
    context = {'news': news,'abs':abs,'length':length}
    return render(request, 'blog_list.html', context)


"""
接受参数：request，news_id
"""
def blog_detail(request,news_id):
    global query_context
    query_context = main()
    news= get_object_or_404(News,id=news_id)
    context = {'news':news
               }
    return render(request, 'blog_detail.html', context)


def search(request):
    global query_context
    query_context = main()
    question = ''
    select = ''
    student_list = []
    if 'search' in request.GET :
        question = request.GET['search']
    if 'select' in request.GET :
        select= request.GET['select']
    error_msg = ''
    print(question)
    if not question:
        error_msg = '请输入关键词'
        return HttpResponse(error_msg)
    query_temp = start_query(select,question,query_context)
    query_vector = query_temp[0]
    token = query_temp[1]
    query_vector_sort = sorted(query_vector,reverse = False)#排序
    news_list = []
    news = News.objects.all()

    news_list_similirity = []
    for i in query_vector_sort:
        if query_vector.get(i) > 0:
            news_list_similirity.append(query_vector.get(i))
    for i in  query_vector_sort:
        for j in news:
            if i == j.title:
                if query_vector.get(i) > 0:
                    news_list.append(j)
    length = len(news_list)
    context = {'token':token,'similar':news_list_similirity,'news': news_list,'length':length}
    return render(request, 'blog_list.html', context)



def merge(n_list1, n_list):
    returnlist = []
    for item in n_list:
        if item in n_list1:
            returnlist.append(item)
    return returnlist
