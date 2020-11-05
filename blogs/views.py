#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
from django.views import generic
from .models import Post
from .models import Comment
from .forms import Post_form
from .forms import CommentForm
from django.shortcuts import redirect
from django.views.generic import FormView
from django.views.generic import UpdateView


from .forms import CreateUserForm
# Create your views here.


from .decorator import unauthenticated_user , allowed_user 
from django.contrib.auth.models import Group

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as djangologout
from django.contrib.auth.forms import UserCreationForm


from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.contrib.auth.models import Group

# def home(request):
# ....return HttpResponse("Hello, world. You're at the blogs homepage.")

# def add_comment(request):
# ....if request.method == 'POST':
# ........form = comments_form(request.POST)
# ........if form.is_valid():
# ............form.save(commit=False)
# ............postname = request.path
# ............form.post = postname.replace('_',' ')
# ............form.save()
# ............return redirect('/')

def redirecthome(request):
    return redirect('/all')


@unauthenticated_user
def signup_login(request):
    form = CreateUserForm()
    if request.method == 'POST':
        if 'signup_pressed' in request.POST:
            form = CreateUserForm(request.POST)
            if form.is_valid():
                usertogroup = form.save()
                user = form.cleaned_data.get('username')
                paswrd = form.cleaned_data.get('password')
                messages.success(request, 'account was created for  '
                                 + user)
                group = Group.objects.get(name='writer')
                usertogroup.groups.add(group)
            else:
                messages.success(request, 'recheck the values')

    if request.method == 'POST':
        if 'login_pressed' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username,
                                password=password)
            if user is not None:
                login(request, user)
                return redirect('/all')
            else:
                messages.info(request, 'Username and password incorrect!')

    return render(request, 'login_signup.html', {'form': form})


def logout(request):
    djangologout(request)
    return redirect('/signup_login')


def genre(request, genre):
    return HttpResponse(request, 'this is genre')


@allowed_user(allowed_roles=['writer', 'pro_writer'])
def add_blog(request):

    if not request.user.is_authenticated:
        return redirect('logon')
    else:
        users_in_group = Group.objects.get(name='pro_writer'
                ).user_set.all()
        user = request.user
        form = Post_form()
        if request.method == 'POST':
            form = Post_form(request.POST or None, request.FILES
                             or None)
            if form.is_valid():
                registor = form.save(commit=False)
                name = registor.title
                registor.author = user
                registor.slug = name.replace(' ', '_')
                if user in users_in_group:
                    registor.status = 1
                else:
                    registor.status = 0
                registor.save()
                return redirect('/')
        return render(request, 'add_blog.html', {'form': form})


def post_detail(request, slug, genre):

    template_name = 'post_detail.html'

    genre = get_object_or_404(Post, genre=genre, slug=slug)
    post = get_object_or_404(Post, slug=slug)

    comments = post.comments.filter(active=True)
    new_comment = None

    # Comment posted

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet

            new_comment = comment_form.save(commit=False)

            # Assign the current post to the comment

            new_comment.post = post

            # Save the comment to the database

            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {
        'post': post,
        'genre': genre,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'name': request.user,
        })


# def search_redirect(request):
#     if request.method == 'GET':
#         value_field = request.GET.('search_value')
#         redirect('/search/' + str(value_field))



def SearchList(request, search_data):
    object_list = Post.objects.filter(content__icontains = search_data , title__icontains = search_data)
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'page': page,
                  'post_list': post_list})



def PostList(request, genre):
    if genre == 'all':
        object_list = \
            Post.objects.filter(status=1).order_by('-created_on')
    else:
        object_list = Post.objects.filter(status=1,
                genre=genre).order_by('-created_on')
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'page': page,
                  'post_list': post_list, 'genre': genre})


# class PostList(generic.ListView):
#     queryset = Post.objects.filter(status=1).order_by('-created_on')
#     template_name = 'index.html'

# class PostDetail(generic.DetailView , FormView):
#     model = Post
#     template_name = 'post_detail.html'
#     form_class = comments_form

# def add_comment_to_post(request, slug):
#     post = get_object_or_404(files, pk=slug)
#     if request.method == "POST":
#         form = comments_form(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.save()
#             return redirect('PostDetail', slug=post.slug)
#     else:
#         form = comments_form()
#     return render(request, 'add_comment.html', {'form': form})
