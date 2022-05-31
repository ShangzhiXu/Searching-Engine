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
返回： 展示所有的在数据库重的用户信息
"""
def list(request):
    global query_context
    query_context = main()
    news = News.objects.all()
    context = {'news': news}
    return render(request, 'blog_list.html', context)


"""
接受参数：request，student_id
返回： 展示一个学生的所有基本信息，包括GPA等，保证主键、外键约束
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
    start_query(select,question,query_context)
    context = {'news': student_list}
    return render(request, 'blog_list.html', context)



def merge(student_list1, student_list):
    returnlist = []
    for item in student_list:
        if item in student_list1:
            returnlist.append(item)
    return returnlist
