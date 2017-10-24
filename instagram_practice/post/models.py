from django.conf import settings
from django.db import models



class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(author=None)

class Post(models.Model):
    author =models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    photo = models.ImageField(upload_to='post')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PostManager()

    class Meta:
        ordering = ['-created_at']

class PostComment(models.Model):
    author =models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    post = models.ForeignKey(Post, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)