from django.shortcuts import render
from blog.models import Comments, Post

# Views

def blog_index(request):
    posts = Post.objects.all().order_by('-created_on')
    return render(request, 'templates/index.html', {'posts': posts})  # ✅

def blog_category(request, category):
    posts = Post.objects.filter(categories__name__contains=category).order_by('-created_on')
    return render(request, 'templates/category.html', {'category': category, 'posts': posts})  # ✅

def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comments.objects.filter(post=post)
    return render(request, 'templates/detail.html', {'post': post, 'comments': comments})  # ✅
