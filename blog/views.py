from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Post, Comment
from blog.forms import CommentForm
from django.contrib import messages
from django.http import HttpResponseRedirect


def get_queryset():
    return Post.objects.filter(status=1, published_date__lte=timezone.now())


def blog_view(request, **kwargs):
    posts = get_queryset().order_by('-published_date')

    if kwargs.get('category_name') is not None:
        posts = posts.filter(category__name=kwargs['category_name'])
    if kwargs.get('author_username') is not None:
        posts = posts.filter(author__username=kwargs['author_username'])
    if kwargs.get('tag_name') is not None:
        posts = posts.filter(tags__name__in=[kwargs['tag_name']])

    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {'posts': page_obj.object_list, 'page_obj': page_obj}
    return render(request, 'blog/blog-home.html', context)


def blog_single(request, pid):
    post = get_object_or_404(Post, pk=pid)

    if post.login_require and not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'پیام شما با موفقیت ثبت شد')
            # Redirect after POST
            return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request, 'خطایی رخ داده است')
            # Redirect after failed POST
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()
        post.counted_views += 1
        post.save()

        next_post = Post.objects.filter(status=1, published_date__gt=post.published_date,
                                        published_date__lte=timezone.now()).order_by('published_date').first()
        prev_post = Post.objects.filter(status=1, published_date__lt=post.published_date,
                                        published_date__lte=timezone.now()).order_by('-published_date').first()

        comments = Comment.objects.filter(post=post.id, approach=True)
        context = {
            'post': post,
            'next_post': next_post,
            'prev_post': prev_post,
            'comments': comments,
            'form': form
        }
        return render(request, 'blog/blog-single.html', context)


def blog_category(request, category_name):
    posts = get_queryset().filter(category__name=category_name)

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
    posts = get_queryset()
    if 's' in request.GET:
        query = request.GET['s']
        posts = posts.filter(content__icontains=query)

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
    post = get_object_or_404(get_queryset(), pk=pid)
    return render(request, 'blog/blog_detail.html', {'post': post})
