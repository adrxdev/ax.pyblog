from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Comments, Post, Profile, Category
from .forms import RegistrationForm, LoginForm, ProfileUpdateForm, CommentForm, ReportForm

# Authentication Views
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('blog_index')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('blog_index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('blog_index')

# Profile Views
@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'registration/profile.html', {'form': form})

# Blog Views
def blog_index(request):
    posts = Post.objects.all().order_by('-created_on')
    return render(request, 'blog/index.html', {'posts': posts})

def blog_category(request, category):
    posts = Post.objects.filter(categories__name__contains=category).order_by('-created_on')
    return render(request, 'blog/category.html', {'category': category, 'posts': posts})

def blog_detail(request, pk):
    post = get_object_or_404(Post, pk = pk)
    comments = Comments.objects.filter(post = post)
    form = CommentForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user.username
            comment.save()
            return redirect('blog_detail', pk=pk)

    return render(request, 'blog/detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


@login_required
def blog_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        category_ids = request.POST.getlist('categories')

        post = Post.objects.create(
            title=title,
            body=body,
            author=request.user
        )

        if category_ids:
            post.categories.set(category_ids)

        if request.FILES.get('image'):
            post.image = request.FILES['image']
            post.save()

        messages.success(request, 'Your post has been created!')
        return redirect('blog_detail', pk=post.pk)

    categories = Category.objects.all()
    return render(request, 'blog/create.html', {'categories': categories})

@login_required
def blog_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == 'POST':
        post.title = request.POST['title']
        post.body = request.POST['body']
        category_ids = request.POST.getlist('categories')

        post.categories.set(category_ids)

        if request.FILES.get('image'):
            post.image = request.FILES['image']

        post.save()
        messages.success(request, 'Your post has been updated!')
        return redirect('blog_detail', pk=post.pk)

    categories = Category.objects.all()
    return render(request, 'blog/edit.html', {'post': post, 'categories': categories})

@login_required
def blog_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    post.delete()
    messages.success(request, 'Your post has been deleted!')
    return redirect('blog_index')


# Report update

@login_required
def report_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.post = post
            report.reported_by = request.user
            report.save()
            messages.success(request, 'Report submitted. Thank you.')
            return redirect('blog_detail', pk=pk)
    else:
        form = ReportForm()

    return render(request, 'blog/report.html', {'form': form, 'post': post})
