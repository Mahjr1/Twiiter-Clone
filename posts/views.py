from tkinter.tix import Form
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from .models import Post
from .forms import PostForm

# Create your views here.
def index(request):
    # If the method is POST
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        #If the form is valid
        if form.is_valid():
            # Yes, Save
            form.save()    


                # Redirect to Home
            return HttpResponseRedirect('/')

        else:
         # No, Show Error
            return HttpResponseRedirect(form.error.as_json())

    #Get all posts, limit  = 20
    posts = Post.objects.all().order_by("-created_at")[:20]
    # Show
    return render(request, 'posts.html',
                    {'posts': posts})

def delete(request, post_id):
    # Find post
    post = Post.objects.get(id = post_id)
    post.delete()
    return HttpResponseRedirect('/' )

def edit(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES, instance= post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect("not valid")
    return render(request, 'edit.html', {"post":post})

def like(request, post_id):
    newLikeCount = Post.objects.get(id=post_id)
    newLikeCount.likecount+=1
    # post.like_count = int(newLikeCount)
    newLikeCount.save()
    return HttpResponseRedirect("/")