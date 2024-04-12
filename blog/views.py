from django.shortcuts import render, get_object_or_404
from blog.models import Post
from django.utils import timezone
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def blog_view(request, **kwargs):
    posts = Post.objects.filter(
        status=1, published_date__lte=timezone.now()).order_by('-published_date')

    if kwargs.get('category_name') is not None:
        posts = posts.filter(category__name=kwargs['category_name'])
    if kwargs.get('author_username') is not None:
        posts = posts.filter(author__username=kwargs['author_username'])
    if kwargs.get('tag_name') is not None:
        posts = posts.filter(tags__name__in=[kwargs['tag_name']])

    paginator = Paginator(posts, 3)
    try:
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        posts = paginator.get_page(1)
    except EmptyPage:
        posts = paginator.get_page(1)
    context = {'posts': page_obj.object_list, 'page_obj': page_obj}
    return render(request, 'blog/blog-home.html', context)


def blog_single(request, pid):
    post = get_object_or_404(Post, pk=pid, status=1,
                             published_date__lte=timezone.now())

    post.counted_views += 1
    post.save()

    next_post = Post.objects.filter(
        status=1, published_date__gt=post.published_date, published_date__lte=timezone.now()).order_by('published_date').first()
    prev_post = Post.objects.filter(
        status=1, published_date__lt=post.published_date, published_date__lte=timezone.now()).order_by('-published_date').first()

    context = {
        'post': post,
        'next_post': next_post,
        'prev_post': prev_post,
    }
    return render(request, 'blog/blog-single.html', context)


def blog_category(request, category_name):
    posts = Post.objects.filter(
        status=1, published_date__lte=timezone.now())
    posts = posts.filter(category__name=category_name)

    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    try:
        page_posts = paginator.page(page_number)
    except PageNotAnInteger:
        page_posts = paginator.page(1)
    except EmptyPage:
        page_posts = paginator.page(paginator.num_pages)

    context = {'posts': page_posts}
    return render(request, 'blog/blog-home.html', context)


def blog_search(request):
    posts = Post.objects.filter(
        status=1, published_date__lte=timezone.now())
    if request.method == 'GET':
        if s := request.GET.get('s'):
            posts = posts.filter(content__contains=s)

    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    try:
        page_posts = paginator.page(page_number)
    except PageNotAnInteger:
        page_posts = paginator.page(1)
    except EmptyPage:
        page_posts = paginator.page(paginator.num_pages)

    context = {'posts': page_posts}
    return render(request, 'blog/blog-home.html', context)


def blog_detail(request, pid):
    post = get_object_or_404(Post, pk=pid, status=1,
                             published_date__lte=timezone.now())
    return render(request, 'blog/blog_detail.html', {'post': post})
