from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView, View
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse

from django import forms

from .models import Post, Comment, User
from .forms import PostForm, CommentForm, UpdatePostForm
from django.contrib import messages
from pdb import set_trace
# Create your views here.

class DashboardView(TemplateView):
    template_name = 'posts/index.html'

    def get(self, request):
        profile_list = User.objects.all()
        posts = Post.objects.all()
        context = {
            'profile_list' : profile_list,
            'posts' : posts
        }
        return render(request, self.template_name, context)

class AddBlogPost(TemplateView):
    def get(self, request):

        if request.user.is_authenticated:
            addform = PostForm()

            return render(request, 'posts/add-blog.html', {'form': addform})
        else:
            return redirect('users:login')

    def post(self, request):
        addform = PostForm(request.POST, request.FILES)

        if addform.is_valid():
            add_blog = addform.save(commit=False)
            add_blog.author = request.user
            addform.save()
            messages.success(request, "Blog posted!")
            return redirect('posts:dashboard')
        else:
            messages.error(request, "Error posting blog!")
            return render(request, 'posts/add-blog.html', {'form': addform})

class UpdateBlogPost(TemplateView):
    template_name = 'posts/edit_post.html'

    def get(self, request, id):

        post = Post.objects.get(id=id)
        data = {
            'title': post.title,
            'content': post.content,
            'picture': post.picture
        }
        form = UpdatePostForm(initial=data)
        context = {
            'post': post,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, id):

        post = Post.objects.get(id=id)
        form = UpdatePostForm(request.POST, request.FILES, instance= post)

        if form.is_valid():
            form = form.save(commit=False)

            form.save()
            messages.success(request, "Blog updated!", extra_tags="update")
            return redirect('posts:postDetail', post.id)

        else:
            form = UpdatePostForm()
            messages.error(request, "Error updating!")
            return redirect('posts:postEdit', post.id)

def delete_Post(request, id):

    post = Post.objects.get(id=id)

    if post.author == request.user:
        post.delete()
        messages.success(request, "Post successfully deleted!")
        return HttpResponseRedirect(reverse('posts:dashboard'))

    return render(request, 'posts/delete_post.html')

def LikeView(request, id):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id = request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('posts:postDetail', args=[id]))

class PostDetailView(TemplateView):
    template_name = 'posts/post_detail.html'

    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        totalLikes = post.total_likes()
        profile_list = User.objects.all()
        isLiked = False
        form = CommentForm()

        if post.likes.filter(id = request.user.id).exists():
            isLiked = True
        context = {
            'totalLikes': totalLikes,
            'isLiked' : isLiked,
            'profile_list' : profile_list,
            'post': post,
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        post = Post.objects.get(id=id)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('posts:postDetail', post.id)

        else:
            form = CommentForm()
            messages.error(request, "Invalid comment!", extra_tags='invalid_comment')
            return redirect('posts:postDetail', post.id)
        