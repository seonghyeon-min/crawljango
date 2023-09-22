from django.shortcuts import render
from .models import Collector
 
def post_view(request) :
    posts  = Collector.objects.all() # db 에 저장된 data를 객체로 저장하여 posts 라는 변수에 저장
    return render(request, 'collector/show.html', {"posts" : posts})