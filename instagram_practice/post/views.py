from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm, CommentForm
from .models import Post, PostComment


def post_list(request):
    posts = Post.objects.all()
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, post_pk):
    # post = Post.objects.get(pk=post_pk)
    # 겟을 했을 때 pk번호가 유효하지 않으면
    # 500번대 서버 에러메시지를 보여주게 되는데
    # 404 메시지를 보여주는게 좀더 정확하기 때문에 아래의 코드로 대체힌다.
    post = get_object_or_404(Post, pk=post_pk)
    comment_form = CommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,
    }
    return render(request, 'post/post_detail.html', context)


def post_create(request):
    if not request.user.is_authenticated:
        return redirect('member:login')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post.objects.create(
                author=request.user,
                photo=form.cleaned_data['photo']
            )
            return redirect('post:post_list')
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'post/post_create.html', context)


def post_delete(request, post_pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        if post.author == request.user:
            post.delete()
            return redirect('post:post_list')
        else:
            raise PermissionDenied('작성자가 아닙니다.')


def comment_create(request, post_pk):
    if not request.user.is_authenticated:
        return redirect('member:login')
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            next = request.GET.get('next', '').strip()
            if next:
                return redirect(next)
            return redirect('post:post_detail', post_pk=post_pk)


def comment_delete(request, comment_pk):
    next_path = request.GET.get('next', '').strip()
    if request.method == 'POST':
        comment = get_object_or_404(PostComment, pk=comment_pk)
        if comment.author == request.user:
            comment.delete()
            if next_path:
                return redirect(next_path)
            return redirect('post:post_detail', post_pk=comment.post.pk)
        else:
            raise PermissionDenied('작성자가 아닙니다')
