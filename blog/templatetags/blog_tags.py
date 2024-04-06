from django import template
from blog.models import Post
from blog.models import Category
from datetime import datetime


register = template.Library()


@register.inclusion_tag('blog/blog-popular-posts.html')
def latestposts():
    posts = Post.objects.filter(status=1).order_by('published_date')[:3]
    return {'posts': posts}


@register.inclusion_tag('blog/blog-post-categories.html')
def postcategories():
    posts = Post.objects.filter(status=1)
    categories = Category.objects.all()
    cat_dict = {}
    for name in categories:
        cat_dict[name] = posts.filter(category=name).count()
    return {'categories': cat_dict}


@register.inclusion_tag('blog/blog-search.html')
def search():
    posts = Post.objects.filter(status=1).order_by('published_date')[:3]
    return {'posts': posts}


@register.inclusion_tag('blog/blog_detail.html')
def blog_detail():
    now = datetime.now()
    posts = Post.objects.filter(
        status=1, published_date__lte=now).order_by('published_date')[:6]
    return {'posts': posts}
