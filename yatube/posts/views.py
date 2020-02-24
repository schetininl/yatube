from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, Comment
from .forms import PostForm, CommentForm
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


@login_required
def new_post(request):
    title = "Добавить запись"
    btn_caption = "Добавить"
    form = PostForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('index')      
    form = PostForm()
    return render(request, 'post_edit.html', {'form': form, 'title': title, 'btn_caption': btn_caption})


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return redirect("post", username=user.username, post_id=post_id)

    title = "Редактировать запись"
    btn_caption = "Сохранить"
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("post", username=request.user.username, post_id=post_id)
    return render(request, 'post_edit.html', {'form': form, 'title': title, 'btn_caption': btn_caption})


@login_required
def post_delete(request, username, post_id):
    if request.user.username != username:
        return redirect(f'/{username}/{post_id}')
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect(f'/{username}')


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
    form = CommentForm()
    comment_list = Comment.objects.filter(post=post).order_by('-created').all()
    context = {'form': form, 'profile': profile, 'post': post, 'posts_count': posts_count, 'comment_list': comment_list}
    return render(request, "post.html", context)


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            return redirect("post", username=request.user.username, post_id=post_id)    
    form = PostForm()


@login_required
def delete_comment(request, username, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user.username == comment.author.username:
        comment.delete()
    return redirect(f'/{username}/{post_id}')

def page_not_found(request, exception):
        return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
        return render(request, "misc/500.html", status=500)