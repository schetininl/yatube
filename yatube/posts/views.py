from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, Comment, Follow
from .forms import PostForm, CommentForm, UserEditForm
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()


def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "index.html", {"page": page, "paginator": paginator})


def group_posts(request, slug): 
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group, "page": page, "paginator": paginator})


@login_required
def new_post(request):
    title = "Добавить запись"
    btn_caption = "Добавить"
    form = PostForm(request.POST or None, files=request.FILES or None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("index")
    form = PostForm()
    return render(request, "post_edit.html", {"form": form, "title": title, "btn_caption": btn_caption})


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return redirect("post", username=user.username, post_id=post_id)

    title = "Редактировать запись"
    btn_caption = "Сохранить"
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("post", username=request.user.username, post_id=post_id)
    return render(request, "post_edit.html", {"form": form, "title": title, "btn_caption": btn_caption, "post": post})


@login_required
def post_delete(request, username, post_id):
    if request.user.username != username:
        return redirect(f"/{username}/{post_id}")
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect("profile", username=username)


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author = profile).order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    posts_count = post_list.count()
    page = paginator.get_page(page_number)
    followers = Follow.objects.filter(author=profile.id).count()
    follows = Follow.objects.filter(user=profile.id).count()
    following = Follow.objects.filter(user=request.user.id, author=profile.id).all()
    context = {"profile": profile, "page": page, "paginator": paginator, "posts_count": posts_count, \
        "followers": followers, "follows": follows, "following": following}
    return render(request, "profile.html", context)


@login_required
def profile_edit(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return redirect("profile", username=user.username)
    form = UserEditForm(request.POST or None, instance=user)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("profile", username=user.username)
    return render(request, "profile_edit.html", {"form": form})
        

def post_view(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id)
    post_list = Post.objects.filter(author = profile).order_by("-pub_date").all()
    posts_count = post_list.count()
    form = CommentForm()
    comment_list = Comment.objects.filter(post=post).order_by("-created").all()
    followers = Follow.objects.filter(author=profile.id).count()
    follows = Follow.objects.filter(user=profile.id).count()
    following = Follow.objects.filter(user=request.user.id, author=profile.id).all()
    context = {
        "form": form, 
        "profile": profile, 
        "post": post,
        "posts_count": posts_count, 
        "comment_list": comment_list,
        "followers": followers, 
        "follows": follows,
        "following": following
    } 
    return render(request, "post.html", context)


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            return redirect("post", username=request.user.username, post_id=post_id)    
    form = PostForm()


@login_required
def comment_delete(request, username, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user.username == comment.author.username:
        comment.delete()
    return redirect("post", username=username, post_id=post_id)  


@login_required
def follow_index(request):
    following = Follow.objects.filter(user=request.user).all()
    author_list = []
    for author in following:
        author_list.append(author.author.id)
    post_list = Post.objects.filter(author__in=author_list).order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "follow.html", {"page": page, "paginator": paginator})


@login_required
def profile_follow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    follow_check = Follow.objects.filter(user=user.id, author=author.id).count()
    if follow_check == 0 and author.id != user.id:
        Follow.objects.create(user=request.user, author=author)
    return redirect("profile", username=username)


@login_required
def profile_unfollow(request, username):
    user = request.user.id
    author = get_object_or_404(User, username=username)
    follow_check = Follow.objects.filter(user=user, author=author.id).count()
    if follow_check == 1:
        Follow.objects.filter(user=request.user, author=author).delete()
    return redirect("profile", username=username)


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
