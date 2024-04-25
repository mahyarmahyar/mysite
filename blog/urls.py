from django.urls import path
from blog.views import *

app_name = 'blog'

urlpatterns = [
    path('', blog_view, name='index'),
    path('detail/<int:pid>/', blog_single, name='single'),
    path('category/<str:category_name>/', blog_category, name='category'),
    path('author/<str:author_username>/', blog_view, name='author'),
    path('tag/<str:tag_name>/', blog_view, name='tag'),
    path('search/', blog_search, name='search'),
    path('<int:pid>/', blog_view, name='blog_detail'),

]
