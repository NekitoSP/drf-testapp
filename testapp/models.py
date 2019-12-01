from django.db import models
from django.db.models import QuerySet
from django.contrib.auth.models import User
import uuid


class Blog(models.Model):
    posts: QuerySet
    title = models.CharField(max_length=100)

    # def posts_str(self):
    #     posts = map(lambda x: x.content, self.posts.all())
    #     return ', '.join(posts)


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=255)


class PostPhoto(models.Model):
    class Meta:
        verbose_name = 'Фотография поста'
        verbose_name_plural = 'Фотографии поста'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(
        Post, null=True, on_delete=models.CASCADE, related_name='photos', blank=True)
    photo = models.ImageField(upload_to='posts', null=True)
    order = models.IntegerField('Порядок', null=True, blank=True)


class Comment(models.Model):
    content = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
