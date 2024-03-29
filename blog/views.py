from django.shortcuts import render, get_object_or_404
from blog.models import Post
from django.utils import timezone
from django.http import HttpResponseNotFound


def blog_view(request):
    posts = Post.objects.filter(status=1, published_date__lte=timezone.now())
    context = {'posts': posts}
    return render(request, 'blog/blog-home.html', context)


def blog_single(request, pid):
    post = get_object_or_404(Post, pk=pid, status=1,
                             published_date__lte=timezone.now())

    post.counted_views += 1
    post.save()

    # Find next and previous published posts
    next_post = Post.objects.filter(
        status=1, published_date__gt=post.published_date).order_by('published_date').first()
    prev_post = Post.objects.filter(
        status=1, published_date__lt=post.published_date).order_by('-published_date').first()

    context = {
        'post': post,
        'next_post': next_post,
        'prev_post': prev_post,
    }
    return render(request, 'blog/blog-single.html', context)
