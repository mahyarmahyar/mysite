from django.db import models
from django.utils import timezone

# Create your models here.


class Post(models.Model):
    # image =
    # author =
    title = models.CharField(max_length=255)
    content = models.TextField()
    # tags =
    # category =
    counted_views = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    published_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-status']

    def __str__(self):
        return self.title
