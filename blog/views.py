from django.shortcuts import render, get_object_or_404
from blog.models import Post
from django.utils import timezone
from django.http import HttpResponseNotFound


def blog_view(request):
    posts = Post.objects.filter(status=1, published_date__lte=timezone.now())
    context = {'posts': posts}
    return render(request, 'blog/blog-home.html', context)


def blog_single(request, pid):
    post = get_object_or_404(Post, pk=pid)
    if post.published_date > timezone.now():
        return HttpResponseNotFound('<h1>404 - Not Found</h1>')
    if not post.status == 1:
        return HttpResponseNotFound('<h1>404 - Not Found</h1>')
    post.counted_views += 1
    post.save()
    context = {'post': post}
    return render(request, 'blog/blog-single.html', context)
