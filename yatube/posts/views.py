from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group
from .forms import PostForm
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page, 'paginator': paginator})


def group_posts(request, slug): 
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group, 'page': page, 'paginator': paginator}) 


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author = profile).order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    posts_count = post_list.count()
    page = paginator.get_page(page_number)
    context = {'profile': profile, 'page': page, 'paginator': paginator, 'posts_count': posts_count}
    return render(request, "profile.html", context)


def post_view(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id)
    post_list = Post.objects.filter(author = profile).order_by('-pub_date').all()
    posts_count = post_list.count()
    context = {'profile': profile, 'post': post, 'posts_count': posts_count}
    return render(request, "post.html", context)


@login_required
def new_post(request):
    title = "Добавить запись"
    btn_caption = "Добавить"
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            n_post = form.save(commit=False)
            n_post.author = request.user
            n_post.save()
            return redirect('index')      
    form = PostForm()
    return render(request, 'new_post.html', {'form': form, 'title': title, 'btn_caption': btn_caption})


def post_edit(request, username, post_id):
    if request.user.username != username:
        return redirect(f'/{username}/{post_id}')

    title = "Редактировать запись"
    btn_caption = "Сохранить"
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            n_post = form.save(commit=False)
            n_post.author = request.user
            n_post.save()
            return redirect(f'/{username}/{post_id}')      
    form = PostForm(instance=post)
    return render(request, 'new_post.html', {'form': form, 'title': title, 'btn_caption': btn_caption, 'post': post})
        

def post_delete(request, username, post_id):
    if request.user.username != username:
        return redirect(f'/{username}/{post_id}')
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect(f'/{username}')
        
