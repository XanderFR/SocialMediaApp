from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostCreateForm, CommentForm
from .models import Post


# Create your views here.
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user  # Get currently logged-in user
            new_item.save()
    else:
        form = PostCreateForm(data=request.POST)
    return render(request, 'posts/create.html', {'form': form})


def feed(request):
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        new_comment = comment_form.save(commit=False)  # Save comment but do not commit
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        new_comment.post = post  # Attach post to comment
        new_comment.save()
    else:
        comment_form = CommentForm()

    posts = Post.objects.all()  # Get all the posts
    logged_user = request.user
    return render(request, 'posts/feed.html', {'posts': posts, 'logged_user': logged_user, 'comment_form': comment_form})


def like_post(request):
    # Get the right post
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    # Like logic
    if post.liked_by.filter(id=request.user.id).exists():
        post.liked_by.remove(request.user)  # Unlike
    else:
        post.liked_by.add(request.user)  # Like
    return redirect('feed')
