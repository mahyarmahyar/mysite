from django.urls import path
from .views import *

app_name = 'projectApp'


urlpatterns = [
    path('', coming_soon_view, name='coming_soon'),
    # This line will catch all other paths
    path('&lt;path:unused_path&gt;/', coming_soon_view),
]

# urlpatterns = [
#    path('', index_view, name='index'),
#    path('about/', about_view, name='about'),
#    path('contact/', contact_view, name='contact'),
#    path('elements/', elements_view, name='elements'),
#    path('newsletter', newsletter_view, name='newsletter'),
# ]
