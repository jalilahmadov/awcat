from django.shortcuts import render,HttpResponse,get_object_or_404,redirect, HttpResponseRedirect, reverse
from django.db.models import F,Count
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Comment, Contact ,News
from gtts import gTTS
from django.core.files.storage import FileSystemStorage
import os
from django.utils.html import strip_tags

class ArticlesView(ListView):
    model = News
    paginate_by = 4
    context_object_name = 'news'
    template_name = 'home.html'
    

def mp3(request,id):
    post = get_object_or_404(News, id=id)
    folder='media/' 
    mytext = post.description
    stripped = strip_tags(mytext)
    mp3name = post.slug
    language = 'en'
    myobj = gTTS(text=stripped, lang=language, slow=False)   
    myobj.save(os.path.join('media', mp3name + ".mp3"))
    return HttpResponseRedirect(post.get_absolute_url())

def detail_view(request, slug):
    post = get_object_or_404(News, slug=slug)
    popular = News.objects.all()[:3]

    response_data = {}

    if request.POST.get('action') == 'comment':
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('comment')
        date = request.POST.get('date')

        response_data['name'] = name
        response_data['comment'] = comment
        response_data['date'] = date
      
        Comment.objects.create(
            name = name,
            email = email,
            comment = comment,
            post = post,
  
        )
        return JsonResponse(response_data)

    if request.POST.get('action') == 'contact':
        email = request.POST.get('email')
        message = request.POST.get('message')

        Contact.objects.create(
            email = email,
            message = message,
            

        )
        response_data['email'] = email
        response_data['message'] = message
        

        return JsonResponse(response_data)


    News.objects.filter(id=post.id).update(views=F('views') + 1)
    comments = Comment.objects.filter(post=post)
    comments_count = Comment.objects.filter(post=post).annotate(book_count=Count('comment'))


    context = {

      'post':post,
      'popular':popular,
      'comments':comments,
      'comments_count':comments_count,
      
    }
    template="detail.html"
    return render(request, template, context)


def contact(request):
    template = "contact.html"
    return render(request, template)


def home(request):
    news = News.objects.all()[:3]
    context = {
        'news':news,
    }
    template = "main.html"
    return render(request, template, context)    

def faq(request):
    template="faq.html";
    return render(request,template)    